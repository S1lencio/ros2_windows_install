import subprocess
import sys
import ctypes

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