@echo off

:: Step 1: Define the Python version and download URLs
set "pythonVersion=3.8.3"
set "pythonDownloadUrl=https://www.python.org/ftp/python/%pythonVersion%/python-%pythonVersion%-amd64.exe"
set "scriptUrl=https://raw.githubusercontent.com/S1lencio/ros2_windows_install/refs/heads/python/install.py"

:: Step 2: Define the installation directory
set "installDir=C:\Python"

:: Step 3: Check if Python is already installed
echo Checking if Python is installed...
where python >nul 2>nul
if %errorlevel% equ 0 (
    echo Python is already installed, skipping installation.
) else (
    :: Step 4: Python is not installed, so download and install Python
    echo Python is not installed, proceeding with installation...
    echo Downloading Python installer...
    bitsadmin.exe /transfer "PythonInstaller" "%pythonDownloadUrl%" "%TEMP%\python-installer.exe"

    echo Installing Python...
    "%TEMP%\python-installer.exe" /quiet InstallAllUsers=1 PrependPath=1 DefaultCustomInstall=1 DefaultPath=%installDir% /wait

    :: Step 5: Clean up the installer
    del "%TEMP%\python-installer.exe" /f /q
)

:: Step 6: Check if the install.py script is already on the Desktop
if not exist "%USERPROFILE%\Desktop\install.py" (
    echo Downloading install.py...
    bitsadmin.exe /transfer "ScriptDownload" "%scriptUrl%" "%USERPROFILE%/Desktop/install.py"
) else (
    echo install.py already exists on Desktop.
)

:: Step 7: Run the install.py script
echo Running the Python script...
python %USERPROFILE%/Desktop/install.py

:: End of script
echo Script execution completed.
pause
