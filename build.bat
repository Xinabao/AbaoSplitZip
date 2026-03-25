@echo off
for /f "delims=" %%V in ('python -c "from core.version import APP_NAME, APP_VERSION; print(APP_NAME + '|' + APP_VERSION)"') do set "APP_META=%%V"
for /f "tokens=1,2 delims=|" %%A in ("%APP_META%") do (
    set "APP_NAME=%%A"
    set "APP_VERSION=%%B"
)
echo === %APP_NAME% Build ===
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.
echo Building exe...
python -m PyInstaller build.spec --clean --noconfirm
echo.
echo Copying Python runtime DLL...
for %%I in ("%~f0\..") do set "SCRIPT_DIR=%%~fI"
for /f "tokens=*" %%P in ('python -c "import sys,os;print(os.path.dirname(sys.executable))"') do (
    copy /Y "%%P\python3*.dll" "%SCRIPT_DIR%\dist\" >nul 2>&1
)
echo.
echo Creating release package...
mkdir "%SCRIPT_DIR%\dist\%APP_NAME%_Release" 2>nul
copy /Y "%SCRIPT_DIR%\dist\%APP_NAME%.exe" "%SCRIPT_DIR%\dist\%APP_NAME%_Release\" >nul
copy /Y "%SCRIPT_DIR%\resources\使用说明.txt" "%SCRIPT_DIR%\dist\%APP_NAME%_Release\" >nul
powershell -Command "Compress-Archive -Path '%SCRIPT_DIR%\dist\%APP_NAME%_Release\*' -DestinationPath '%SCRIPT_DIR%\dist\%APP_NAME%_v%APP_VERSION%.zip' -Force"
echo.
echo Done!
echo   EXE: dist\%APP_NAME%.exe
echo   Release: dist\%APP_NAME%_v%APP_VERSION%.zip
pause
