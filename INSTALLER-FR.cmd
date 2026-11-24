@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if exist "%~dp0INSTALLER-FR.exe" (
  start "" "%~dp0INSTALLER-FR.exe"
  exit /b 0
)
where py >nul 2>nul
if errorlevel 1 goto python
py -3 "%~dp0installation\fr_manager.py" gui
goto done
:python
where python >nul 2>nul
if errorlevel 1 goto missing
python "%~dp0installation\fr_manager.py" gui
goto done
:missing
echo Python 3 avec Tkinter est necessaire. Voir installation\README.md.
:done
pause
