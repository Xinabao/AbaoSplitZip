@echo off
echo === AbaoZip Build ===
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.
echo Building exe...
python -m PyInstaller build.spec --clean --noconfirm
echo.
echo Copying Python runtime DLL...
copy /Y "%~dp0..\..\..\..\Python314\python314.dll" "%~dp0dist\AbaoZip\" >nul 2>&1
for %%I in ("%~f0\..") do set "SCRIPT_DIR=%%~fI"
for /f "tokens=*" %%P in ('python -c "import sys,os;print(os.path.dirname(sys.executable))"') do (
    copy /Y "%%P\python3*.dll" "%SCRIPT_DIR%\dist\AbaoZip\" >nul 2>&1
)
echo.
echo Done! Output: dist\AbaoZip\AbaoZip.exe
pause
