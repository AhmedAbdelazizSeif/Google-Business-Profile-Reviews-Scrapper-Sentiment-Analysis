# Setup Script for Google Reviews Sentiment Analysis

Write-Host "=" -repeat 80 -ForegroundColor Cyan
Write-Host "Google Reviews Sentiment Analysis - Setup" -ForegroundColor Cyan
Write-Host "=" -repeat 80 -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "[1/5] Checking Python installation..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Python found: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.8 or higher." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host ""
Write-Host "[2/5] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  Virtual environment already exists" -ForegroundColor Gray
} else {
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "[3/5] Activating virtual environment..." -ForegroundColor Yellow
& "venv\Scripts\Activate.ps1"
Write-Host "✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host ""
Write-Host "[4/5] Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip | Out-Null
pip install -r requirements.txt
Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Download NLTK data
Write-Host ""
Write-Host "[5/5] Downloading NLTK data..." -ForegroundColor Yellow
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('vader_lexicon', quiet=True)"
Write-Host "✓ NLTK data downloaded" -ForegroundColor Green

# Create necessary directories
Write-Host ""
Write-Host "Creating output directories..." -ForegroundColor Yellow
$dirs = @("output\reviews", "output\reports")
foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    }
}
Write-Host "✓ Directories ready" -ForegroundColor Green

# Final message
Write-Host ""
Write-Host "=" -repeat 80 -ForegroundColor Cyan
Write-Host "✓ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=" -repeat 80 -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Update configuration in src/config.py" -ForegroundColor White
Write-Host "  2. Place your logo in assets/logo.png" -ForegroundColor White
Write-Host "  3. Start Chrome: .\scripts\start_chrome.ps1" -ForegroundColor White
Write-Host "  4. Run pipeline: python scripts\run_full_pipeline.py" -ForegroundColor White
Write-Host ""
Write-Host "For detailed instructions, see README.md" -ForegroundColor Gray
Write-Host ""
