@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 goto use_python
set "AZERTY_PYTHON=py -3"
goto menu
:use_python
where python >nul 2>nul
if errorlevel 1 goto missing
set "AZERTY_PYTHON=python"
:menu
echo Incursion Red River - AZERTY 0.1.0 beta
echo 1. Preview / Apercu
echo 2. Install / Installer - game must be closed
echo 3. Restore / Restaurer
echo Q. Quitter
choice /c 123Q /n /m "Choix : "
if errorlevel 4 exit /b 0
if errorlevel 3 goto restore
if errorlevel 2 goto install
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
