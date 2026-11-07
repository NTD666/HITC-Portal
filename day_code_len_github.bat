@echo off
chcp 65001 >nul
title Đẩy Code Lên GitHub - HITC Portal
color 0B

echo =======================================================================
echo    🚀 ĐANG ĐẨY TOÀN BỘ CODE MỚI LÊN GITHUB (NTD666/HITC-Portal)
echo =======================================================================
echo.

git push origin main

if %errorlevel% equ 0 (
    echo.
    echo =======================================================================
    echo    ✅ CHÚC MỪNG! ĐÃ ĐẨY CODE LÊN GITHUB THÀNH CÔNG RỰC RỠ!
    echo    👉 Xem repo của bạn tại: https://github.com/NTD666/HITC-Portal
    echo =======================================================================
) else (
    echo.
    echo [THÔNG BÁO] Nếu chưa đăng nhập, vui lòng đăng nhập trên cửa sổ vừa hiện ra.
)

echo.
pause
