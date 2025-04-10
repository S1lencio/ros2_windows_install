import subprocess
import sys
import ctypes
import os
import urllib.request
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
    install_ros2()

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

        urllib.request.urlretrieve(url, installer_path)

        print(f"Downloaded Visual Studio installer to {installer_path}")

        return installer_path
    except:
        done(1, "Failed to download Visual Studio installer.")

def install_visual_studio(installer_path):
    try:
        # Command to install Visual Studio with the Desktop Development with C++ workload
        command = [
            installer_path,
            "modify",
            "install",
            "--passive",
            "--norestart",
            "--force",
            "--add", "Microsoft.VisualStudio.Component.CoreEditor",
            "--add", "Microsoft.VisualStudio.Workload.CoreEditor",
            "--add", "Microsoft.VisualStudio.Component.NuGet",
            "--add", "Microsoft.VisualStudio.Component.Roslyn.Compiler",
            "--add", "Microsoft.VisualStudio.Component.Roslyn.LanguageServices",
            "--add", "Microsoft.VisualStudio.ComponentGroup.WebToolsExtensions",
            "--add", "Microsoft.VisualStudio.Component.TypeScript.4.3",
            "--add", "Microsoft.VisualStudio.Component.JavaScript.TypeScript",
            "--add", "Microsoft.Component.MSBuild",
            "--add", "Microsoft.VisualStudio.Component.TextTemplating",
            "--add", "Microsoft.VisualStudio.Component.Debugger.JustInTime",
            "--add", "Component.Microsoft.VisualStudio.LiveShare",
            "--add", "Microsoft.VisualStudio.Component.IntelliCode",
            "--add", "Microsoft.VisualStudio.Component.VC.CoreIde",
            "--add", "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
            "--add", "Microsoft.VisualStudio.Component.Graphics.Tools",
            "--add", "Microsoft.VisualStudio.Component.VC.DiagnosticTools",
            "--add", "Microsoft.VisualStudio.Component.Windows10SDK.19041",
            "--add", "Microsoft.VisualStudio.Component.VC.Redist.14.Latest",
            "--add", "Microsoft.VisualStudio.ComponentGroup.NativeDesktop.Core",
            "--add", "Microsoft.VisualStudio.Component.VC.ATL",
            "--add", "Microsoft.VisualStudio.Component.VC.TestAdapterForBoostTest",
            "--add", "Microsoft.VisualStudio.Component.VC.TestAdapterForGoogleTest",
            "--add", "Microsoft.VisualStudio.Component.VC.ASAN",
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

        print(f"Downloaded OpenCV to {opencv_temp_path}")

        urllib.request.urlretrieve(url, opencv_temp_path)

        with zipfile.ZipFile(opencv_temp_path, 'r') as zip_ref:
            zip_ref.extractall(opencv_path)

        print(f"Extracted OpenCV to {opencv_path}")

        subprocess.check_call(["setx", "/m", "OpenCV_DIR", opencv_path])
        set_path(r"C:\opencv\x64\vc16\bin")

        print("OpenCV installation completed.")
    except:
        done(1, "Failed to install OpenCV")

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

        urllib.request.urlretrieve(url + "asio.1.12.1.nupkg", asio_path)
        urllib.request.urlretrieve(url + "bullet.3.17.nupkg", bullet_path)
        urllib.request.urlretrieve(url + "cunit.2.1.3.nupkg", cunit_path)
        urllib.request.urlretrieve(url + "eigen.3.3.4.nupkg", eigen_path)
        urllib.request.urlretrieve(url + "tinyxml2.6.0.0.nupkg", tinyxml_path)

        print(f"Downloaded dependencies to {os.getenv('TEMP')}")

        subprocess.check_call([choco, "install", "-y", "-s", os.getenv("TEMP"), "asio", "cunit", "eigen", "tinyxml2", "bullet"])

        print("Chocolatey dependencies installation complete.")
    except:
        done(1, f"Failed to install choco dependencies")

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

        # Needs this to extract .7z files
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-U", "py7zr"])

        print("Python packages installation complete.")
    except subprocess.CalledProcessError as e:
        done(1, f"Failed to install Python packages: {e}")

def install_xmllint():
    import py7zr
    try:
        url = "https://www.zlatkovic.com/pub/libxml/64bit/"
        xmllint_path = r"C:\xmllint"

        print()
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
        done(1, "Failed to download xmllint dependencies.")

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

        urllib.request.urlretrieve(url, ros2_temp_path)

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
