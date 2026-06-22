@echo off
title KHI KHOI DONG HE THONG THI DUA THANH XUAN
echo =====================================================
echo 🌱 DANG KHOI DONG SERVER BACKEND PYTHON (FASTAPI)...
echo =====================================================
:: Lệnh này sẽ mở một cửa sổ CMD mới để chạy Python độc lập ở cổng 8000
 start cmd /k "uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
 start cmd /k "python run.py"
echo.
echo =====================================================
echo 🌍 DANG KHOI DONG GIAO DIEN FRONTEND FLUTTER WEB...
echo =====================================================
flutter run -d web-server --web-hostname 0.0.0.0 --web-port 63763
pause