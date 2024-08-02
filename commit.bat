@echo off
REM Check if a commit message is provided
IF "%1"=="" (
    echo Usage: commit.bat "commit message"
    exit /b 1
)

REM Navigate to your repository (optional)
REM cd C:\path\to\your\repository

REM Stage all changes
git add .

REM Commit with the provided message
git commit -m "%1"

REM Push to the remote repository
git push

echo Commit and push completed.
pause
