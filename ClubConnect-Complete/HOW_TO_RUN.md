# How to Run ClubConnect

This document explains the different ways to run the ClubConnect application.

## Option 1: Using simple_run.py (Recommended for Beginners)

The `simple_run.py` file is a standalone script that initializes the database and runs the application in one step.

### Using Command Prompt (cmd.exe)

1. Double-click on `simple-start.bat`

OR

1. Open Command Prompt
2. Navigate to the ClubConnect-Complete directory
3. Run: `python simple_run.py`

### Using PowerShell

1. Right-click on `simple-start.ps1` and select "Run with PowerShell"

OR

1. Open PowerShell
2. Navigate to the ClubConnect-Complete directory
3. Run: `.\simple-start.ps1`

OR

1. Open PowerShell
2. Navigate to the ClubConnect-Complete directory
3. Run: `python simple_run.py`

## Option 2: Using Flask CLI (Advanced)

This method uses the Flask command-line interface to run the application.

### Using Command Prompt (cmd.exe)

1. Double-click on `flask-start.bat`

OR

1. Open Command Prompt
2. Navigate to the ClubConnect-Complete directory
3. Run:
   ```
   set FLASK_APP=run.py
   flask run
   ```

### Using PowerShell

1. Right-click on `flask-start.ps1` and select "Run with PowerShell"

OR

1. Open PowerShell
2. Navigate to the ClubConnect-Complete directory
3. Run:
   ```
   $env:FLASK_APP = "run.py"
   flask run
   ```

## Accessing the Application

Once the application is running:

1. Open your web browser
2. Go to: http://localhost:5000
3. Login credentials: 
   - Username: admin
   - Password: admin123

## Stopping the Application

To stop the running application, press `Ctrl+C` in the terminal window.
