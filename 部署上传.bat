@echo off
chcp 65001 >nul
set SERVER_IP=1.12.47.237
set SERVER_USER=ubuntu

cd /d "%~dp0"

echo ========================================
echo   Deploying to %SERVER_IP% ...
echo ========================================
echo.
echo [1/2] Converting CSV to JS ...
python csv2js.py
if %errorlevel% neq 0 (
    echo [FAIL] Conversion failed.
    pause
    exit /b 1
)
echo.
echo [2/2] Uploading files ...
scp products.csv products.js index.html %SERVER_USER%@%SERVER_IP%:/var/www/everstock/
scp -r img %SERVER_USER%@%SERVER_IP%:/var/www/everstock/
echo.
echo Done! Visit: http://%SERVER_IP%
pause
