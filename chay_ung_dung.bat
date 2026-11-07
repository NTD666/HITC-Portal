@echo off
chcp 65001 >nul
title HITC Portal - Cổng Thông Tin Sinh Viên HITC TP.HCM
color 0A

echo =======================================================================
echo    🏫 TRƯỜNG CAO ĐẲNG CÔNG THƯƠNG THÀNH PHỐ HỒ CHÍ MINH (HITC)
echo    🚀 HỆ THỐNG HITC PORTAL - KHỞI ĐỘNG TỰ ĐỘNG
echo =======================================================================
echo.

:: 1. Kiểm tra Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [LỖI] Máy tính chưa cài đặt Python hoặc chưa tick "Add Python to PATH"!
    echo Vui lòng tải và cài đặt Python từ https://www.python.org/
    pause
    exit /b
)

echo [1/3] Đang kiểm tra thư viện cần thiết...
python -c "import streamlit, pandas, altair" >nul 2>&1
if %errorlevel% neq 0 (
    echo [THÔNG BÁO] Chưa tìm thấy đầy đủ thư viện. Đang tự động cài đặt (Streamlit, Pandas, Altair)...
    python -m pip install streamlit pandas altair
    if %errorlevel% neq 0 (
        echo [LỖI] Không thể cài đặt thư viện. Vui lòng kiểm tra kết nối mạng!
        pause
        exit /b
    )
)

echo [2/3] Chạy kiểm thử hệ thống...
python test_app.py
if %errorlevel% neq 0 (
    echo [CẢNH BÁO] Kiểm thử có vấn đề nhưng vẫn tiếp tục khởi động...
)

echo.
echo [3/3] Đang khởi chạy HITC Portal trên trình duyệt...
echo =======================================================================
echo    Trang web sẽ tự động mở tại: http://localhost:8501
echo    (Nhấn Ctrl + C tại cửa sổ này khi muốn dừng ứng dụng)
echo =======================================================================
echo.

python -m streamlit run app.py

pause
