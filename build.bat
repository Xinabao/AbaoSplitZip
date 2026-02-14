@echo off
echo === AbaoSplitZip Build ===
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
mkdir "%SCRIPT_DIR%\dist\AbaoSplitZip_Release" 2>nul
copy /Y "%SCRIPT_DIR%\dist\AbaoSplitZip.exe" "%SCRIPT_DIR%\dist\AbaoSplitZip_Release\" >nul
copy /Y "%SCRIPT_DIR%\resources\使用说明.txt" "%SCRIPT_DIR%\dist\AbaoSplitZip_Release\" >nul
powershell -Command "Compress-Archive -Path '%SCRIPT_DIR%\dist\AbaoSplitZip_Release\*' -DestinationPath '%SCRIPT_DIR%\dist\AbaoSplitZip_v1.1.0.zip' -Force"
echo.
echo Done!
echo   EXE: dist\AbaoSplitZip.exe
echo   Release: dist\AbaoSplitZip_v1.1.0.zip
pause
