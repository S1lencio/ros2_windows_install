import subprocess
import sys
import ctypes
import os
import urllib.request
import zipfile

import py7zr

# Helper functions
def set_path(new_path):
    try:
        powershell_command = f'''
        $PATH = [System.Environment]::GetEnvironmentVariable('PATH', 'Machine')
        if (-not($PATH.Contains("{new_path}"))) {{
            [System.Environment]::SetEnvironmentVariable('PATH', $PATH + ";{new_path}", 'Machine')
        }}
        '''

        # Run the PowerShell command with subprocess
        subprocess.check_call(["powershell", "-Command", powershell_command])
    except subprocess.CalledProcessError as e:
        print(f"Failed to set PATH variable: {e}")
        input()
        sys.exit(1)

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
    install_choco_dependencies()
    upgrade_pip_setuptools()
    install_python_packages()
    install_xmllint()
    install_qt5()
    install_rqt()

def install_chocolatey():
    # Check if Chocolatey is already installed
    try:
        subprocess.call(["choco", "--version"])
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
        subprocess.check_call(["setx", "/m", "OPENSSL_CONF", openssl_conf_path])

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
    subprocess.check_call(command)
    print("Visual Studio installation completed.")

def install_opencv():
    url = "https://github.com/ros2/ros2/releases/download/opencv-archives/opencv-3.4.6-vc16.VS2019.zip"

    print(f"Downloading OpenCV from {url}...")

    opencv_temp_path = os.path.join(os.getenv("TEMP"), "opencv-3.4.6-vc16.VS2019.zip")
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

def install_choco_dependencies():
    try:
        url = "https://github.com/ros2/choco-packages/releases/tag/2022-03-15"

        print("Installing Chocolatey dependencies...")

        asio_path = os.path.join(os.getenv("TEMP"), "asio.1.12.1.nupkg")
        bullet_path = os.path.join(os.getenv("TEMP"), "bullet.3.17.nupkg")
        cunit_path = os.path.join(os.getenv("TEMP"), "cunit.2.1.3.nupkg")
        eigen_path = os.path.join(os.getenv("TEMP"), "eigen.3.3.4.nupkg")
        tinyxml_path = os.path.join(os.getenv("TEMP"), "tinyxml2.6.0.0.nupkg")

        urllib.request.urlretrieve(url + "asio.1.12.1.nupkg", asio_path)
        urllib.request.urlretrieve(url + "bullet.3.17.nupkg", bullet_path)
        urllib.request.urlretrieve(url + "cunit.2.1.3.nupkg", cunit_path)
        urllib.request.urlretrieve(url + "eigen.3.3.4.nupkg", eigen_path)
        urllib.request.urlretrieve(url + "tinyxml2.6.0.0.nupkg", tinyxml_path)

        print(f"Downloaded dependencies to {os.getenv('TEMP')}")

        subprocess.check_call(["choco", "install", "-y", "-s", os.getenv("TEMP"), "asio", "cunit", "eigen", "tinyxml2", "bullet"])

        print("Chocolatey dependencies installation complete.")
    except:
        print(f"Failed to install choco dependencies")
        input()
        sys.exit(1)

def upgrade_pip_setuptools():
    try:
        print("Upgrading pip and setuptools...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "pip", "setuptools==59.6.0"])

        print("pip and setuptools upgraded successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to upgrade pip and setuptools: {e}")
        input()
        sys.exit(1)

def install_python_packages():
    try:
        print("Installing Python packages...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U",
                               "catkin_pkg", "cryptography", "empy", "importlib-metadata", "jsonschema", "lark==1.1.1",
                               "lxml", "matplotlib", "netifaces", "numpy", "opencv-python", "PyQt5", "pillow", "psutil",
                               "pycairo", "pydot", "pyparsing==2.4.7", "pytest", "pyyaml", "rosdistro"
                               ])

        # Needs this to extract .7z files
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "py7zr"])

        print("Python packages installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Python packages: {e}")
        input()
        sys.exit(1)

def install_xmllint():
    try:
        url = "https://www.zlatkovic.com/pub/libxml/64bit/"
        xmllint_path = r"C:\xmllint"

        print("Installing xmllint...")

        libxml2 = os.path.join(os.getenv("TEMP"), "libxml2-2.9.3-win32-x86_64.7z")
        iconv = os.path.join(os.getenv("TEMP"), "iconv-1.14-win32-x86_64.7z")
        zlib = os.path.join(os.getenv("TEMP"), "zlib-1.2.8-win32-x86_64.7z")

        urllib.request.urlretrieve(url + "libxml2-2.9.3-win32-x86_64.7z", libxml2)
        urllib.request.urlretrieve(url + "iconv-1.14-win32-x86_64.7z", iconv)
        urllib.request.urlretrieve(url + "zlib-1.2.8-win32-x86_64.7z", zlib)

        print(f"Downloaded xmllint dependencies to {os.getenv('TEMP')}")

        print("Extracting libxml2...")
        with py7zr.SevenZipFile(libxml2, mode='r') as archive:
            archive.extractall(xmllint_path)

        print("Extracting iconv...")
        with py7zr.SevenZipFile(iconv, mode='r') as archive:
            archive.extractall(xmllint_path)

        print("Extracting zlib...")
        with py7zr.SevenZipFile(zlib, mode='r') as archive:
            archive.extractall(xmllint_path)

        print("Extracted xmllint dependencies")

        set_path(xmllint_path + r"\bin")

        print("Xmllint installation complete.")
    except:
        print("Failed to download xmllint dependencies.")
        input()
        sys.exit(1)

def install_qt5():
    try:
        print("Installing Qt5...")

        subprocess.check_call(["choco", "install", "-y", "aqt", "qtcreator"])

        subprocess.check_call(["aqt", "install-qt", "windows", "desktop", "5.12.12", "win64_msvc2017_64", "--modules ", "debug_info", "--output-dir", r"C:\Qt5"])

        subprocess.check_call(["setx", "/m", "Qt5_DIR", r"C:\Qt\5.12.12\msvc2017_64"])
        subprocess.check_call(["setx", "/m", "QT_QPA_PLATFORM_PLUGIN_PATH", r"C:\Qt\5.12.12\msvc2017_64\plugins\platforms"])

        print("Qt5 installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install Qt5: {e}")
        input()
        sys.exit(1)

def install_rqt():
    try:
        print("Installing rqt...")

        subprocess.check_call(["choco", "install", "-y", "graphviz"])

        set_path(r"C:\Program Files\Graphviz\bin")

        print("rqt installation complete.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install rqt: {e}")
        input()
        sys.exit(1)

# Run the installation function
main()

# Wait for user input before closing the script
input()