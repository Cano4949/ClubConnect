# ClubConnect - Simple Run (PowerShell Version)
Write-Host "================================================"
Write-Host "ClubConnect - Simple Run"
Write-Host "================================================"
Write-Host ""

# Change to the directory where this script is located
Set-Location -Path $PSScriptRoot

# Start the application
Write-Host "Starting ClubConnect with simple_run.py..."
Write-Host ""
python simple_run.py

# Pause at the end
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
