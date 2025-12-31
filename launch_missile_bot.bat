@echo off
REM Change directory to the script location
cd /d "%~dp0"
REM Launch in Windows Terminal
wt -d . python missile_bot.py
pause
