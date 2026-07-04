@echo off
chcp 65001 >nul
cd /d %~dp0

echo ========================================
echo   EverStock Garments
echo ========================================
echo.
echo [1/2] Converting CSV to JS ...
python csv2js.py
if %errorlevel% neq 0 (
    echo.
    echo [FAIL] Conversion failed.
    pause
    exit /b 1
)
echo [2/2] Opening browser ...
start "" "index.html"
echo.
echo Done!
pause
