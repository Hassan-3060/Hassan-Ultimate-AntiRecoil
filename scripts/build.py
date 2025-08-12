"""
Build Script for Hassan Ultimate Anti-Recoil v7.0
Automated build process for creating standalone executables
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
import PyInstaller.__main__


def build_executable():
    """Build standalone executable using PyInstaller."""
    
    print("🚀 Building Hassan Ultimate Anti-Recoil v7.0...")
    
    # Clean previous builds
    if Path("dist").exists():
        shutil.rmtree("dist")
    if Path("build").exists():
        shutil.rmtree("build")
    
    # PyInstaller arguments
    args = [
        "main.py",
        "--name=Hassan-Ultimate-AntiRecoil-v7.0",
        "--onefile",
        "--windowed",
        "--add-data=config;config",
        "--add-data=assets;assets",
        "--add-data=src;src",
        "--hidden-import=pynput",
        "--hidden-import=customtkinter",
        "--hidden-import=PIL",
        "--hidden-import=numpy",
        "--hidden-import=matplotlib",
        "--hidden-import=sklearn",
        "--hidden-import=fastapi",
        "--hidden-import=uvicorn",
        "--icon=assets/icons/app_icon.ico",
        "--version-file=version_info.txt",
        "--distpath=dist",
        "--workpath=build",
        "--clean"
    ]
    
    try:
        PyInstaller.__main__.run(args)
        print("✅ Build completed successfully!")
        print(f"📦 Executable created: dist/Hassan-Ultimate-AntiRecoil-v7.0.exe")
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True


def create_installer():
    """Create installer package."""
    print("📦 Creating installer package...")
    
    # Create installer directory structure
    installer_dir = Path("installer")
    installer_dir.mkdir(exist_ok=True)
    
    # Copy executable
    exe_path = Path("dist/Hassan-Ultimate-AntiRecoil-v7.0.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, installer_dir)
    
    # Copy documentation
    docs_dir = installer_dir / "docs"
    docs_dir.mkdir(exist_ok=True)
    
    if Path("docs").exists():
        for doc_file in Path("docs").glob("*.md"):
            shutil.copy2(doc_file, docs_dir)
    
    # Copy config templates
    config_dir = installer_dir / "config"
    config_dir.mkdir(exist_ok=True)
    
    if Path("config").exists():
        for config_file in Path("config").glob("*.json"):
            shutil.copy2(config_file, config_dir)
    
    # Create batch files
    create_launcher_scripts(installer_dir)
    
    print("✅ Installer package created in 'installer' directory")


def create_launcher_scripts(installer_dir):
    """Create launcher scripts."""
    
    # Windows launcher
    launcher_bat = installer_dir / "Launch-Hassan-AntiRecoil.bat"
    with open(launcher_bat, 'w') as f:
        f.write("""@echo off
title Hassan Ultimate Anti-Recoil v7.0
echo Starting Hassan Ultimate Anti-Recoil v7.0...
echo.
Hassan-Ultimate-AntiRecoil-v7.0.exe
pause
""")
    
    # Admin launcher
    admin_bat = installer_dir / "Launch-As-Admin.bat"
    with open(admin_bat, 'w') as f:
        f.write("""@echo off
title Hassan Ultimate Anti-Recoil v7.0 (Administrator)
echo Starting Hassan Ultimate Anti-Recoil v7.0 as Administrator...
echo.
powershell -Command "Start-Process 'Hassan-Ultimate-AntiRecoil-v7.0.exe' -Verb RunAs"
""")
    
    # Install dependencies script
    install_deps = installer_dir / "Install-Dependencies.bat"
    with open(install_deps, 'w') as f:
        f.write("""@echo off
title Install Dependencies
echo Installing Python dependencies for Hassan Ultimate Anti-Recoil...
echo.
python -m pip install --upgrade pip
pip install pynput customtkinter pillow numpy matplotlib scikit-learn fastapi uvicorn
echo.
echo Dependencies installed successfully!
pause
""")


def create_version_info():
    """Create version info file for PyInstaller."""
    version_info = """# UTF-8
#
# For more details about fixed file info 'ffi' see:
# http://msdn.microsoft.com/en-us/library/ms646997.aspx
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=(7,0,0,0),
    prodvers=(7,0,0,0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        u'040904B0',
        [StringStruct(u'CompanyName', u'Hassan-3060'),
        StringStruct(u'FileDescription', u'Hassan Ultimate Anti-Recoil v7.0 Professional Edition'),
        StringStruct(u'FileVersion', u'7.0.0.0'),
        StringStruct(u'InternalName', u'Hassan-Ultimate-AntiRecoil'),
        StringStruct(u'LegalCopyright', u'Copyright (C) 2024 Hassan-3060'),
        StringStruct(u'OriginalFilename', u'Hassan-Ultimate-AntiRecoil-v7.0.exe'),
        StringStruct(u'ProductName', u'Hassan Ultimate Anti-Recoil'),
        StringStruct(u'ProductVersion', u'7.0.0 Professional Edition')])
      ]), 
    VarFileInfo([VarStruct(u'Translation', [1033, 1200])])
  ]
)"""
    
    with open("version_info.txt", 'w') as f:
        f.write(version_info)


def main():
    """Main build process."""
    print("🏗️  Hassan Ultimate Anti-Recoil v7.0 Build System")
    print("=" * 50)
    
    # Change to script directory
    os.chdir(Path(__file__).parent)
    
    # Create version info
    create_version_info()
    
    # Build executable
    if build_executable():
        # Create installer package
        create_installer()
        
        print("\n🎉 Build process completed successfully!")
        print("📁 Files created:")
        print("   - dist/Hassan-Ultimate-AntiRecoil-v7.0.exe")
        print("   - installer/ (complete package)")
        print("\n🚀 Ready for distribution!")
    else:
        print("\n❌ Build process failed!")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())