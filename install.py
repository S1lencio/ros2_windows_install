import subprocess
import sys
import ctypes
import os
import zipfile

# Helper functions
def done(code: int, msg: str):
    print(msg)
    input()
    sys.exit(code)

choco = r"C:\ProgramData\chocolatey\bin\choco.exe"

def set_path(new_path):
    try:
        if new_path not in os.environ["PATH"]:
            os.environ["PATH"] += f";{new_path}"
    except subprocess.CalledProcessError as e:
        done(1, "Failed to set PATH variable: {e}")

def is_admin():
    return ctypes.windll.shell32.IsUserAnAdmin() == 1

def run_as_admin():
    if not is_admin():
        print("Not running as administrator. Trying to elevate...")
        # Relaunch the script with elevated permissions
        subprocess.run(["runas", "/user:Administrator", sys.executable] + sys.argv)
        sys.exit()

def download_file(url, dest_path):
    import requests
    try:
        # Send a GET request to the URL
        response = requests.get(url, stream=True, verify=True)  # verify=True checks SSL certificates
        response.raise_for_status()  # Check if the request was successful (status code 200)

        # Write the content to the destination path
        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

# Main function
def main():
    # Escalate to admin if not already
    run_as_admin()

    upgrade_pip_setuptools()
    install_installer_packages()
    install_chocolatey()
    install_cpp()
    install_openssl()
    installer_path = download_visual_studio_installer()
    install_visual_studio(installer_path)
    install_opencv()
    install_cmake()
    install_choco_dependencies()
    install_python_packages()
    install_xmllint()
    install_qt5()
    install_rqt()
    install_ros2()

def install_installer_packages():
    try:
        print()
        print("Installing packages needed for installer...")

        # Needs this for web downloads
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "requests"])

        # Needs this for .7z files
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "pyunpack"])

        print("Packages installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install requests: {e}")

def install_chocolatey():
    # Check if Chocolatey is already installed
    try:
        subprocess.call([choco, "--version"])
        print("Chocolatey is already installed.")
        return
    except FileNotFoundError:
        pass  # Chocolatey is not installed, proceed with installation

    try:
        print()
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
        done(1, f"Failed to install Chocolatey: {e}")

def install_cpp():
    try:
        print()
        print("Installing Visual C++ Redistributables...")

        # Install
        subprocess.check_call([choco, "install", "-y", "vcredist2013", "vcredist140"])

        print("Visual C++ Redistributables installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install Visual C++ Redistributables: {e}")

def install_openssl():
    try:
        print()
        print("Installing OpenSSL...")

        # Install
        subprocess.check_call([choco, "install", "-y", "openssl", "--version 1.1.1.2100"])

        # Set environment variable
        openssl_conf_path = r"C:\Program Files\OpenSSL-Win64\bin\openssl.cfg"
        subprocess.check_call(["setx", "/m", "OPENSSL_CONF", openssl_conf_path])

        # Set PATH
        set_path(r'C:\Program Files\OpenSSL-Win64\bin')

        print("OpenSSL installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install OpenSSL: {e}")

def download_visual_studio_installer():
    try:
        url = "https://aka.ms/vs/16/release/vs_community.exe"
        installer_path = os.path.join(os.getenv("TEMP"), "vs_installer.exe")

        # Download the installer
        print()
        print(f"Downloading Visual Studio installer from {url}...")

        download_file(url, installer_path)

        print(f"Downloaded Visual Studio installer to {installer_path}")

        return installer_path
    except Exception as e:
        done(1, f"Failed to download Visual Studio installer: {e}")

def install_visual_studio(installer_path):
    try:
        # Command to install Visual Studio with the Desktop Development with C++ workload
        command = [
            installer_path,
            "install",
            "--wait",
            "--passive",
            "--norestart",
            "--force",
            "--theme", "dark",
            "--add", "Microsoft.VisualStudio.Workload.NativeDesktop",
            "--remove", "Microsoft.VisualStudio.Component.CMake",
            "--remove", "Microsoft.VisualStudio.Component.VC.CMake.Project",
        ]

        # Run the installer command
        print()
        print("Installing Visual Studio...")
        subprocess.check_call(command)
        print("Visual Studio installation completed.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install Visual Studio: {e}")

def install_opencv():
    try:
        url = "https://github.com/ros2/ros2/releases/download/opencv-archives/opencv-3.4.6-vc16.VS2019.zip"

        print()
        print(f"Downloading OpenCV from {url}...")

        opencv_temp_path = os.path.join(os.getenv("TEMP"), "opencv-3.4.6-vc16.VS2019.zip")
        opencv_path = r"C:\opencv"

        download_file(url, opencv_temp_path)

        print(f"Downloaded OpenCV to {opencv_temp_path}")

        with zipfile.ZipFile(opencv_temp_path, 'r') as zip_ref:
            zip_ref.extractall(opencv_path)

        print(f"Extracted OpenCV to {opencv_path}")

        subprocess.check_call(["setx", "/m", "OpenCV_DIR", opencv_path])
        set_path(r"C:\opencv\x64\vc16\bin")

        print("OpenCV installation completed.")
    except Exception as e:
        done(1, f"Failed to install OpenCV: {e}")

def install_cmake():
    try:
        print()
        print("Installing CMake...")

        # Install
        subprocess.check_call([choco, "install", "-y", "cmake"])

        print("CMake installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install CMake: {e}")

def install_choco_dependencies():
    try:
        url = "https://github.com/ros2/choco-packages/releases/download/2022-03-15/"

        print()
        print("Installing Chocolatey dependencies...")

        asio_path = os.path.join(os.getenv("TEMP"), "asio.1.12.1.nupkg")
        bullet_path = os.path.join(os.getenv("TEMP"), "bullet.3.17.nupkg")
        cunit_path = os.path.join(os.getenv("TEMP"), "cunit.2.1.3.nupkg")
        eigen_path = os.path.join(os.getenv("TEMP"), "eigen.3.3.4.nupkg")
        tinyxml_path = os.path.join(os.getenv("TEMP"), "tinyxml2.6.0.0.nupkg")

        download_file(url + "asio.1.12.1.nupkg", asio_path)
        download_file(url + "bullet.3.17.nupkg", bullet_path)
        download_file(url + "cunit.2.1.3.nupkg", cunit_path)
        download_file(url + "eigen.3.3.4.nupkg", eigen_path)
        download_file(url + "tinyxml2.6.0.0.nupkg", tinyxml_path)

        print(f"Downloaded dependencies to {os.getenv('TEMP')}")

        subprocess.check_call([choco, "install", "-y", "-s", os.getenv("TEMP"), "asio", "cunit", "eigen", "tinyxml2", "bullet"])

        print("Chocolatey dependencies installation complete.")
    except Exception as e:
        done(1, f"Failed to install choco dependencies: {e}")

def upgrade_pip_setuptools():
    try:
        print()
        print("Upgrading pip and setuptools...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "pip", "setuptools==59.6.0"])

        print("pip and setuptools upgraded successfully.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to upgrade pip and setuptools: {e}")

def install_python_packages():
    try:
        print()
        print("Installing Python packages...")

        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U",
                               "catkin_pkg", "cryptography", "empy", "importlib-metadata", "jsonschema", "lark==1.1.1",
                               "lxml", "matplotlib", "netifaces", "numpy", "opencv-python", "PyQt5", "pillow", "psutil",
                               "pycairo", "pydot", "pyparsing==2.4.7", "pytest", "pyyaml", "rosdistro"
                               ])

        print("Python packages installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install Python packages: {e}")

def install_xmllint():
    from pyunpack import Archive
    try:
        url = "https://www.zlatkovic.com/pub/libxml/64bit/"
        xmllint_path = r"C:\xmllint"

        print()
        print("Installing xmllint...")

        libxml2 = os.path.join(os.getenv("TEMP"), "libxml2-2.9.3-win32-x86_64.7z")
        iconv = os.path.join(os.getenv("TEMP"), "iconv-1.14-win32-x86_64.7z")
        zlib = os.path.join(os.getenv("TEMP"), "zlib-1.2.8-win32-x86_64.7z")

        download_file(url + "libxml2-2.9.3-win32-x86_64.7z", libxml2)
        download_file(url + "iconv-1.14-win32-x86_64.7z", iconv)
        download_file(url + "zlib-1.2.8-win32-x86_64.7z", zlib)

        print(f"Downloaded xmllint dependencies to {os.getenv('TEMP')}")

        print("Extracting libxml2...")

        Archive(libxml2).extractall(xmllint_path)
        Archive(iconv).extractall(xmllint_path)
        Archive(zlib).extractall(xmllint_path)

        print("Extracted xmllint dependencies")

        set_path(xmllint_path + r"\bin")

        print("Xmllint installation complete.")
    except Exception as e:
        done(1, f"Failed to download xmllint dependencies: {e}")

def install_qt5():
    try:
        print()
        print("Installing Qt5...")

        subprocess.check_call([choco, "install", "-y", "aqt", "qtcreator"])

        subprocess.check_call(["aqt", "install-qt", "windows", "desktop", "5.12.12", "win64_msvc2017_64", "--modules ", "debug_info", "--output-dir", r"C:\Qt5"])

        subprocess.check_call(["setx", "/m", "Qt5_DIR", r"C:\Qt\5.12.12\msvc2017_64"])
        subprocess.check_call(["setx", "/m", "QT_QPA_PLATFORM_PLUGIN_PATH", r"C:\Qt\5.12.12\msvc2017_64\plugins\platforms"])

        print("Qt5 installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install Qt5: {e}")

def install_rqt():
    try:
        print()
        print("Installing rqt...")

        subprocess.check_call([choco, "install", "-y", "graphviz"])

        set_path(r"C:\Program Files\Graphviz\bin")

        print("rqt installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install rqt: {e}")

def install_ros2():
    try:
        url = "https://github.com/ros2/ros2/releases/download/release-jazzy-20241223/ros2-jazzy-20241223-windows-release-amd64.zip"

        print()
        print(f"Downloading ROS2 from {url}...")

        ros2_temp_path = os.path.join(os.getenv("TEMP"), "ros2.zip")
        ros2_path = r"C:\dev\ros2_jazzy"

        download_file(url, ros2_temp_path)

        print(f"Downloaded ROS2 to {ros2_temp_path}")

        with zipfile.ZipFile(ros2_temp_path, 'r') as zip_ref:
            zip_ref.extractall(ros2_path)

        print("ROS2 installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install ROS2: {e}")

# Run the installation function
main()

# Wait for user input before closing the script
done(0, "ROS2 Installation complete.")
