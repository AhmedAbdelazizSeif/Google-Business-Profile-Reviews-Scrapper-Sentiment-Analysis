# PowerShell script to start Chrome with remote debugging
Write-Host "Starting Chrome with Remote Debugging..." -ForegroundColor Cyan
Write-Host ""

# Close existing Chrome instances
Write-Host "Closing existing Chrome instances..." -ForegroundColor Yellow
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Create profile directory if it doesn't exist
$profileDir = "C:\selenium\ChromeProfile"
if (-not (Test-Path $profileDir)) {
    New-Item -ItemType Directory -Path $profileDir -Force | Out-Null
    Write-Host "Created profile directory: $profileDir" -ForegroundColor Green
}

# Find Chrome executable
$chromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$chromePath = $null
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        $chromePath = $path
        break
    }
}

if (-not $chromePath) {
    Write-Host "ERROR: Chrome executable not found!" -ForegroundColor Red
    Write-Host "Please install Google Chrome or specify the correct path." -ForegroundColor Red
    exit 1
}

# Start Chrome with remote debugging
Write-Host "Starting Chrome from: $chromePath" -ForegroundColor Green
Start-Process -FilePath $chromePath -ArgumentList "--remote-debugging-port=9222", "--user-data-dir=`"$profileDir`""

Write-Host ""
Write-Host "Chrome started with remote debugging on port 9222" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Log in to Google Business in the Chrome window" -ForegroundColor White
Write-Host "  2. Navigate to your reviews page" -ForegroundColor White
Write-Host "  3. Run the scraper" -ForegroundColor White
Write-Host ""
