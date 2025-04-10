@echo off

:: Define the Python version and download URLs
set "pythonVersion=3.8.3"
set "pythonDownloadUrl=https://www.python.org/ftp/python/%pythonVersion%/python-%pythonVersion%-amd64.exe"
set "scriptUrl=https://raw.githubusercontent.com/S1lencio/ros2_windows_install/refs/heads/python/install.py"

:: Check if Python is already installed
echo Checking if Python is installed...
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Python is already installed, skipping installation.
) else (
    :: Python is not installed, so download and install Python
    echo Python is not installed, proceeding with installation...
    echo Downloading Python installer...
    curl -L -o "%TEMP%\python-installer.exe" "%pythonDownloadUrl%"

    echo Installing Python...
    "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 TargetDir="C:\Python38" /wait

    :: Clean up the installer
    del "%TEMP%\python-installer.exe" /f /q
)

:: Check if the install.py script is already on the Desktop
if not exist "%USERPROFILE%\Desktop\install.py" (
    echo Downloading install.py...
    curl -L -o "%USERPROFILE%\Desktop\install.py" "%scriptUrl%"
) else (
    echo install.py already exists on Desktop.
)

:: Run the install.py script
echo Running the Python script...
"C:\Program Files\Python38\python.exe" "%USERPROFILE%\Desktop\install.py"

:: End of script
echo Script execution completed.
pause
