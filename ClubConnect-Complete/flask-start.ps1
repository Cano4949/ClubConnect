# ClubConnect - Flask Run (PowerShell Version)
Write-Host "================================================"
Write-Host "ClubConnect - Flask Run"
Write-Host "================================================"
Write-Host ""

# Change to the directory where this script is located
Set-Location -Path $PSScriptRoot

# Set environment variables
Write-Host "Setting environment variables..."
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"
$env:FLASK_DEBUG = 1

# Start Flask
Write-Host "Starting Flask..."
Write-Host ""
Write-Host "Open your browser and go to:"
Write-Host "http://localhost:5000"
Write-Host ""
Write-Host "Login: admin / admin123"
Write-Host ""
Write-Host "Press Ctrl+C to stop."
Write-Host "================================================"

# Run Flask
flask run

# Pause at the end
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
