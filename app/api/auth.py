from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy import select
import bcrypt
from datetime import datetime, timedelta, timezone

from app.database import get_async_db, AsyncSession
from app.models.user import User
from app.models.refresh_token import RefreshToken
from app.schemas.auth_schema import LoginRequest, RefreshRequest, LogoutRequest
from app.core.jwt_handler import create_access_token, create_refresh_token
from app.dependencies.auth_dependency import get_current_user_id
from jose import jwt, JWTError
from app.core.config import JWT_SECRET_KEY, JWT_ALGORITHM

router = APIRouter()

@router.get("/test")
async def auth_test():
    return {"auth": "ok"}

@router.post("/login")
async def login(data: LoginRequest, db: AsyncSession = Depends(get_async_db)):
    # 🔎 1. Truy vấn tìm kiếm tài khoản bất đồng bộ trực tiếp từ Database Postgres
    result = await db.execute(select(User).where(User.username == data.username))
    user = result.scalar_one_or_none()

    # Nếu không tìm thấy tên đăng nhập, trả về thông báo lỗi đồng bộ bảo mật cho giao diện Flutter
    if not user:
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác.")

    # 🔒 2. KIỂM TRA MẬT KHẨU ĐỘNG TỪ DATABASE (Đã loại bỏ hoàn toàn mã gán cứng)
    # Tiến hành giải mã và đối chiếu mật khẩu chữ thường người dùng nhập với chuỗi băm bcrypt trong DB
    try:
        is_password_correct = bcrypt.checkpw(
            data.password.encode('utf-8'),      # Mật khẩu chữ thường từ Flutter gửi lên
            user.password_hash.encode('utf-8')  # Chuỗi băm bảo mật lưu trong cột password_hash của Database
        )
    except Exception:
        # Đề phòng trường hợp chuỗi password_hash trong DB lỗi định dạng ký tự
        is_password_correct = False

    if not is_password_correct:
        raise HTTPException(status_code=401, detail="Tài khoản hoặc mật khẩu không chính xác.")

    # 🎟️ 3. Khởi tạo Token khi thông tin xác thực hoàn toàn trùng khớp
    access_token = create_access_token(user.user_id)
    refresh_token = create_refresh_token(user.user_id)

    # Sử dụng timestamp làm ID hoặc để DB tự sinh (đảm bảo kiểu naive datetime cho Postgres)
    now_naive = datetime.utcnow()
    db_token = RefreshToken(
        token_id=int(now_naive.timestamp()),
        user_id=user.user_id,
        refresh_token=refresh_token,
        expires_at=now_naive + timedelta(days=30),
        created_at=now_naive,
        is_revoked=False
    )

    db.add(db_token)
    await db.flush()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user_id": user.user_id,
        "username": user.username,
        "full_name": user.full_name
    }

@router.get("/profile")
async def profile(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(User).where(User.user_id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "user_id": user.user_id,
        "username": user.username,
        "full_name": user.full_name,
        "role_id": user.role_id,
        "school_id": user.school_id,
        "department_id": user.department_id
    }

@router.post("/refresh")
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(RefreshToken).where(RefreshToken.refresh_token == data.refresh_token))
    token_row = result.scalar_one_or_none()

    if not token_row:
        raise HTTPException(status_code=401, detail="Refresh token not found")

    if token_row.is_revoked:
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    if token_row.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Refresh token expired")

    try:
        payload = jwt.decode(data.refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user_id = int(payload["sub"])
    except JWTError:
        raise HTTPException(status_code=401, detail="Refresh token invalid")

    access_token = create_access_token(user_id)
    return {"access_token": access_token, "token_type": "bearer"}
    
@router.post("/logout")
async def logout(data: LogoutRequest, db: AsyncSession = Depends(get_async_db)):
    result = await db.execute(select(RefreshToken).where(RefreshToken.refresh_token == data.refresh_token))
    token_row = result.scalar_one_or_none()

    if not token_row:
        raise HTTPException(status_code=404, detail="Refresh token not found")

    token_row.is_revoked = True
    await db.flush()

    return {"message": "Logout success"}