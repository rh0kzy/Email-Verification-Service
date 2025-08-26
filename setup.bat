@echo off
echo Installing required packages for Email Verification Service...
echo.

C:/Users/PC/AppData/Local/Microsoft/WindowsApps/python3.12.exe -m pip install python-dotenv

echo.
echo Installation complete!
echo.
echo To run the application:
echo   GUI Version: python gui_app.py
echo   CLI Version: python cli_app.py
echo.
pause
