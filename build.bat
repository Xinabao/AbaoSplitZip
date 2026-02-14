@echo off
echo === AbaoZip Build ===
echo.
echo Installing dependencies...
pip install -r requirements.txt --quiet
echo.
echo Building exe...
python -m PyInstaller build.spec --clean --noconfirm
echo.
echo Done! Output: dist\AbaoZip\AbaoZip.exe
pause
