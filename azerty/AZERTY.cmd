@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
if exist "%~dp0AZERTY.exe" (
  start "" "%~dp0AZERTY.exe"
  exit /b 0
)
where py >nul 2>nul
if errorlevel 1 goto use_python
set "AZERTY_PYTHON=py -3"
goto menu
:use_python
where python >nul 2>nul
if errorlevel 1 goto missing
set "AZERTY_PYTHON=python"
:menu
echo Incursion Red River - AZERTY 0.3.0 beta
echo 0. Interface graphique
echo 1. Preview / Apercu
echo 2. Install / Installer - game must be closed
echo 3. Restore / Restaurer
echo Q. Quitter
choice /c 0123Q /n /m "Choix : "
if errorlevel 5 exit /b 0
if errorlevel 4 goto restore
if errorlevel 3 goto install
if errorlevel 2 goto preview
%AZERTY_PYTHON% "%~dp0interface.py"
goto done
:preview
%AZERTY_PYTHON% "%~dp0azerty.py" preview
goto done
:install
%AZERTY_PYTHON% "%~dp0azerty.py" install
goto done
:restore
%AZERTY_PYTHON% "%~dp0azerty.py" restore
goto done
:missing
echo Python 3.9 or newer is required. See LISEZ-MOI.md.
:done
pause
