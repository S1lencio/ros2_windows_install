import subprocess
import sys
import ctypes
import os
import winreg as reg

# Helper functions
def set_path(new_path):
    # Open the registry key for system-wide environment variables
    key = reg.OpenKey(reg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment", 0, reg.KEY_WRITE)

    # Get the current PATH
    current_path, _ = reg.QueryValueEx(key, "Path")

    # Add the new directory to the PATH if it's not already there
    if new_path not in current_path:
        new_path_value = current_path + ";" + new_path
        reg.SetValueEx(key, "Path", 0, reg.REG_EXPAND_SZ, new_path_value)
        print(f"Successfully added {new_path} to PATH.")
    else:
        print(f"{new_path} is already in the PATH.")

    # Close the registry key
    reg.CloseKey(key)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

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
        subprocess.check_call(["choco", "install", "-y", "vcredist2013", "vcredist140"])
        print("Visual C++ Redistributables installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Visual C++ Redistributables: {e}")
        input()
        sys.exit(1)

def install_openssl():
    try:
        print("Installing OpenSSL...")
        subprocess.check_call(["choco", "install", "-y", "openssl", "--version 1.1.1.2100"])
        set_path(r'C:\Program Files\OpenSSL-Win64\bin')
        print("OpenSSL installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install OpenSSL: {e}")
        input()
        sys.exit(1)

# Run the installation function
main()

# Wait for user input before closing the script
input()