from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.report_repository import ReportRepository

class ReportService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def generate_monthly_school_report(self, year: int, month: int):
        """
        Lấy danh sách điểm thi đua và tự động gán hạng (rank) cho từng nhân sự
        """
        raw_leaderboard = await ReportRepository.get_school_leaderboard(self.db, year, month)
        
        processed_report = []
        for index, row in enumerate(raw_leaderboard):
            processed_report.append({
                "rank": index + 1,  # Hạng 1, 2, 3... dựa trên thứ tự sắp xếp giảm dần
                "user_id": row.user_id,
                "full_name": row.full_name,
                "department_id": row.department_id,
                "total_score": float(row.total_score)
            })
            
        return processed_report