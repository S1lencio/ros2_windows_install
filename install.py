import subprocess
import sys
import ctypes
import os
import urllib.request
import zipfile

# Helper functions
def set_path(new_path):
    powershell_command = f'''
    $PATH = [System.Environment]::GetEnvironmentVariable('PATH', 'Machine')
    if (-not($PATH.Contains("{new_path}"))) {{
        [System.Environment]::SetEnvironmentVariable('PATH', $PATH + ";{new_path}", 'Machine')
    }}
    '''

    # Run the PowerShell command with subprocess
    subprocess.call(["powershell", "-Command", powershell_command])

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def run_as_admin():
    if not is_admin():
        print("Not running as administrator. Trying to elevate...")
        # Relaunch the script with elevated permissions
        subprocess.run(["runas", "/user:Administrator", sys.executable] + sys.argv)
        sys.exit()

# Main function
def main():
    # Escalate to admin if not already
    run_as_admin()

    install_chocolatey()
    install_cpp()
    install_openssl()
    installer_path = download_visual_studio_installer()
    install_visual_studio(installer_path)
    install_opencv()
    install_cmake()

def install_chocolatey():
    # Check if Chocolatey is already installed
    try:
        subprocess.check_call(["choco", "--version"])
        print("Chocolatey is already installed.")
        return
    except FileNotFoundError:
        pass  # Chocolatey is not installed, proceed with installation

    try:
        print("Installing Chocolatey...")

        install_command = [
            "powershell",
            "-ExecutionPolicy", "Bypass",
            "-NoProfile",
            "-Command",
            "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
        ]

        subprocess.check_call(install_command)
        print("Chocolatey installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Chocolatey: {e}")
        input()
        sys.exit(1)

def install_cpp():
    try:
        print("Installing Visual C++ Redistributables...")

        # Install
        subprocess.check_call(["choco", "install", "-y", "vcredist2013", "vcredist140"])

        print("Visual C++ Redistributables installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Visual C++ Redistributables: {e}")
        input()
        sys.exit(1)

def install_openssl():
    try:
        print("Installing OpenSSL...")

        # Install
        subprocess.check_call(["choco", "install", "-y", "openssl", "--version 1.1.1.2100"])

        # Set environment variable
        openssl_conf_path = r"C:\Program Files\OpenSSL-Win64\bin\openssl.cfg"
        subprocess.call(["setx", "/m", "OPENSSL_CONF", openssl_conf_path])

        # Set PATH
        set_path(r'C:\Program Files\OpenSSL-Win64\bin')

        print("OpenSSL installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install OpenSSL: {e}")
        input()
        sys.exit(1)

def download_visual_studio_installer():
    url = "https://aka.ms/vs/16/release/vs_community.exe"
    installer_path = os.path.join(os.getenv("TEMP"), "vs_installer.exe")

    # Download the installer
    print(f"Downloading Visual Studio installer from {url}...")
    urllib.request.urlretrieve(url, installer_path)
    print(f"Downloaded Visual Studio installer to {installer_path}")
    return installer_path

def install_visual_studio(installer_path):
    # Command to install Visual Studio with the Desktop Development with C++ workload
    command = [
        installer_path,
        "modify",
        "--path cache=" + os.getenv("TEMP"),
        "--add", "Microsoft.VisualStudio.Workload.NativeDesktop",
        "--remove", "Microsoft.VisualStudio.Component.CMake",
        "--remove", "Microsoft.VisualStudio.Component.VC.CMake.Project",
        "--passive",
        "--includeRecommended",
        "--norestart",
        "--force"
    ]

    # Run the installer command
    print("Installing Visual Studio...")
    subprocess.call(command)
    print("Visual Studio installation completed.")

def install_opencv():
    url = "https://github.com/ros2/ros2/releases/download/opencv-archives/opencv-3.4.6-vc16.VS2019.zip"

    print(f"Downloading OpenCV from {url}...")

    opencv_temp_path = os.path.join(os.getenv("TEMP"), "opencv.zip")
    opencv_path = r"C:\opencv"

    print(f"Downloaded OpenCV to {opencv_temp_path}")

    urllib.request.urlretrieve(url, opencv_temp_path)

    with zipfile.ZipFile(opencv_temp_path, 'r') as zip_ref:
        zip_ref.extractall(opencv_path)

    print(f"Extracted OpenCV to {opencv_path}")

    subprocess.call(["setx", "/m", "OpenCV_DIR", opencv_path])
    set_path(r"C:\opencv\x64\vc16\bin")

    print("OpenCV installation completed.")

def install_cmake():
    try:
        print("Installing CMake...")

        # Install
        subprocess.check_call(["choco", "install", "-y", "cmake"])

        print("CMake installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install CMake: {e}")
        input()
        sys.exit(1)

# Run the installation function
main()

# Wait for user input before closing the script
input()