import subprocess
import sys
import ctypes
import os

def main():
    # Check if the script is run with admin privileges
    if not is_admin():
        print("This script requires administrative privileges. Please run as administrator.")
        sys.exit(1)

    # Install Chocolatey
    install_chocolatey()

def is_admin():
    try:
        _admin = os.getuid() == 0
    except AttributeError:
        _admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return _admin

def install_chocolatey():
    # Check if Chocolatey is already installed
    try:
        subprocess.check_call(["choco", "--version"])
        print("Chocolatey is already installed.")
        return
    except subprocess.CalledProcessError:
        pass  # Chocolatey is not installed, proceed with installation

    # Step 1: Run the PowerShell script to install Chocolatey
    install_command = [
        "powershell",
        "-ExecutionPolicy", "Bypass",
        "-NoProfile",
        "-Command",
        "[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]::Tls12; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))"
    ]

    try:
        print("Installing Chocolatey...")
        subprocess.check_call(install_command)
        print("Chocolatey installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Chocolatey: {e}")
        sys.exit(1)

# Run the installation function
main()