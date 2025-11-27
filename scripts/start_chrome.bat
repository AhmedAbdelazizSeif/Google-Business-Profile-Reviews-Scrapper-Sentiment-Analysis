@echo off
echo Starting Chrome with Remote Debugging...
echo.
echo This will open Chrome with your profile and enable remote debugging.
echo You can then run the Python scraper script.
echo.

REM Close existing Chrome instances
taskkill /F /IM chrome.exe 2>nul
timeout /t 2 /nobreak >nul

REM Create profile directory if it doesn't exist
if not exist "C:\selenium\ChromeProfile" mkdir "C:\selenium\ChromeProfile"

REM Start Chrome with remote debugging
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"

echo.
echo Chrome started with remote debugging on port 9222
echo Now you can:
echo   1. Log in to Google Business in Chrome
echo   2. Navigate to your reviews page
echo   3. Run: python scrape_reviews.py
echo.
pause
