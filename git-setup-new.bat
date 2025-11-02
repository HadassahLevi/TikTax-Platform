@echo off
cd /d C:\TikTax

REM Remove old git
rmdir /s /q .git 2>nul

REM Initialize new git
git init
git add .
git commit -m "🎉 Initial commit: Frontend project setup with React 18.2 + TypeScript + Tailwind CSS + RTL support"
git branch -M main
git remote add origin https://github.com/HadassahLevi/TikTax-Platform.git
git push -u origin main

echo.
echo ========================================
echo Git setup completed successfully!
echo Repository: TikTax-Platform
echo ========================================
pause
