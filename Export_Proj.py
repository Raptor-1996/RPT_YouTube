"""
Export_Proj.py - RPT YouTube Export Tool
Developer: Raptor96
GitHub: https://github.com/Raptor-1996/
"""

import os
import sys
import shutil
import subprocess
import json
from pathlib import Path
import zipfile
import stat
import time

APP_NAME = "RPT_YouTube"
APP_VERSION = "3.0.0"
AUTHOR = "Raptor96"
GITHUB_URL = "https://github.com/Raptor-1996/"
MAIN_SCRIPT = "RPT_YouTube_v3.py"

BASE_DIR = Path(__file__).parent.absolute()
OUTPUT_DIR = BASE_DIR / "RPT_YouTube_Releases"
DIST_DIR = BASE_DIR / "dist"
BUILD_DIR = BASE_DIR / "build"

def clean_dir(path):
    if Path(path).exists():
        shutil.rmtree(path)
    Path(path).mkdir(parents=True, exist_ok=True)

def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
        return True
    except Exception as e:
        print(f"Error copying {src}: {e}")
        return False

def copy_dir(src, dst):
    try:
        if Path(dst).exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        return True
    except Exception as e:
        print(f"Error copying {src}: {e}")
        return False

def write_file(path, content):
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    except Exception as e:
        print(f"Error writing {path}: {e}")
        return False

def get_main_script():
    main_script = BASE_DIR / MAIN_SCRIPT
    if main_script.exists():
        return main_script
    for alt in ["RPT_YouTube.py", "main.py"]:
        alt_path = BASE_DIR / alt
        if alt_path.exists():
            return alt_path
    return None

def create_info_files(output_dir):
    readme_content = f"""========================================
{APP_NAME} v{APP_VERSION}
========================================

Developer: {AUTHOR}
GitHub: {GITHUB_URL}

Features:
- Video Download: 144p to 2160p
- Audio Download: MP3 64-320 kbps
- Dark/Light Themes
- English/Persian Languages
- Real-time Progress
- Auto Organization

How to Use:
1. Launch the application
2. Paste YouTube URL
3. Click "Check"
4. Select format and quality
5. Click "Download"

Made with Love by {AUTHOR}
"""
    write_file(output_dir / "README.txt", readme_content)
    return True

def check_dependencies():
    print("\n" + "="*60)
    print("Checking dependencies...")
    print("="*60)
    missing = []
    # Check PyInstaller via import
    try:
        import PyInstaller
        print(f"✅ PyInstaller: OK")
    except:
        print(f"❌ PyInstaller: NOT FOUND")
        missing.append('PyInstaller')
    # Check pip
    try:
        subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, check=True)
        print(f"✅ pip: OK")
    except:
        print(f"❌ pip: NOT FOUND")
        missing.append('pip')
    # Check python
    print(f"✅ python: OK")
    if get_main_script():
        print(f"✅ Main script: OK")
    else:
        print(f"❌ Main script: NOT FOUND")
        missing.append('main_script')
    if (BASE_DIR / "assets").exists():
        print(f"✅ Assets: OK")
    else:
        print(f"❌ Assets: NOT FOUND")
        missing.append('assets')
    if missing:
        print(f"\nMissing: {', '.join(missing)}")
        return False
    return True

def build_windows_exe():
    print("\n" + "="*60)
    print("Building Windows EXE...")
    print("="*60)
    exe_output = OUTPUT_DIR / "Windows" / "RPT_YouTube_Portable"
    clean_dir(exe_output)
    main_script = get_main_script()
    if not main_script:
        return False
    assets_dir = BASE_DIR / "assets"
    if not assets_dir.exists():
        return False
    # Install pyinstaller if needed
    try:
        import PyInstaller
    except:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], capture_output=True)
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    # Use python -m PyInstaller instead of direct command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile", "--windowed",
        "--name", APP_NAME,
        "--icon", str(assets_dir / "icon.ico"),
        "--add-data", f"assets{os.pathsep}assets",
        "--hidden-import", "customtkinter",
        "--hidden-import", "PIL",
        "--hidden-import", "yt_dlp",
        "--hidden-import", "pygame",
        "--collect-all", "customtkinter",
        str(main_script)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"PyInstaller error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False
    exe_src = DIST_DIR / f"{APP_NAME}.exe"
    if exe_src.exists():
        copy_file(exe_src, exe_output / f"{APP_NAME}.exe")
        copy_dir(assets_dir, exe_output / "assets")
        batch = f"""@echo off
echo {APP_NAME} v{APP_VERSION}
echo Developer: {AUTHOR}
echo.
start "" "%~dp0{APP_NAME}.exe"
"""
        write_file(exe_output / "Run_RPT_YouTube.bat", batch)
        create_info_files(exe_output)
        size = exe_src.stat().st_size / (1024 * 1024)
        print(f"✅ EXE created: {exe_output}")
        print(f"📦 Size: {size:.2f} MB")
        return True
    print("❌ EXE not found!")
    return False

def build_linux_deb():
    print("\n" + "="*60)
    print("Building Linux DEB...")
    print("="*60)
    deb_output = OUTPUT_DIR / "Linux"
    clean_dir(deb_output)
    main_script = get_main_script()
    if not main_script:
        return False
    assets_dir = BASE_DIR / "assets"
    if not assets_dir.exists():
        return False
    deb_root = deb_output / "rpt-youtube"
    deb_root.mkdir(parents=True)
    debian_dir = deb_root / "DEBIAN"
    debian_dir.mkdir()
    control = f"""Package: rpt-youtube
Version: {APP_VERSION}
Section: utils
Priority: optional
Architecture: all
Depends: python3, python3-pip, ffmpeg
Maintainer: {AUTHOR}
Description: RPT YouTube Downloader
"""
    write_file(debian_dir / "control", control)
    postinst = f"""#!/bin/bash
echo "RPT YouTube v{APP_VERSION} installed!"
echo "Run: rpt-youtube"
"""
    write_file(debian_dir / "postinst", postinst)
    os.chmod(debian_dir / "postinst", 0o755)
    app_dir = deb_root / "usr" / "share" / "rpt-youtube"
    app_dir.mkdir(parents=True)
    copy_file(main_script, app_dir / "RPT_YouTube.py")
    copy_dir(assets_dir, app_dir / "assets")
    launcher = app_dir / "rpt-youtube.py"
    launcher.write_text("#!/usr/bin/env python3\nimport RPT_YouTube")
    os.chmod(launcher, 0o755)
    desktop_dir = deb_root / "usr" / "share" / "applications"
    desktop_dir.mkdir(parents=True)
    desktop = f"""[Desktop Entry]
Name=RPT YouTube
Exec=python3 /usr/share/rpt-youtube/RPT_YouTube.py
Icon=/usr/share/rpt-youtube/assets/icon.png
Terminal=false
Type=Application
Categories=AudioVideo;
"""
    write_file(desktop_dir / "rpt-youtube.desktop", desktop)
    create_info_files(deb_output)
    try:
        subprocess.run(["dpkg-deb", "--build", str(deb_root)], cwd=deb_output, check=True)
    except:
        print("⚠️ dpkg-deb not available (Linux only)")
        return False
    deb_file = deb_output / "rpt-youtube.deb"
    if deb_file.exists():
        new_name = deb_output / f"rpt-youtube_{APP_VERSION}_all.deb"
        shutil.move(str(deb_file), str(new_name))
        size = new_name.stat().st_size / (1024 * 1024)
        print(f"✅ DEB created: {new_name}")
        print(f"📦 Size: {size:.2f} MB")
        return True
    return False

def build_github_release():
    print("\n" + "="*60)
    print("Building GitHub structure...")
    print("="*60)
    github_output = OUTPUT_DIR / "GitHub"
    clean_dir(github_output)
    win_src = OUTPUT_DIR / "Windows" / "RPT_YouTube_Portable"
    if win_src.exists():
        copy_dir(win_src, github_output / "RPT_YouTube_Portable")
    linux_src = OUTPUT_DIR / "Linux"
    if linux_src.exists():
        copy_dir(linux_src, github_output / "Linux")
    releases_dir = github_output / "releases"
    releases_dir.mkdir(exist_ok=True)
    releases = f"""RPT YouTube v{APP_VERSION}
Windows: RPT_YouTube.exe
Linux: rpt-youtube_{APP_VERSION}_all.deb
Developer: {AUTHOR}
"""
    write_file(releases_dir / "RELEASES.txt", releases)
    readme = f"""# RPT YouTube v{APP_VERSION}
Developer: {AUTHOR}
GitHub: {GITHUB_URL}

Features:
- Video/Audio Download
- Multiple Qualities
- Dark/Light Themes
- Bilingual
- Real-time Progress

Quick Start:
1. Download the app
2. Paste YouTube URL
3. Click Check
4. Select format
5. Click Download

Made with Love by {AUTHOR}
"""
    write_file(github_output / "README.md", readme)
    print(f"✅ GitHub structure created: {github_output}")
    return True

def create_archives():
    print("\n" + "="*60)
    print("Creating archives...")
    print("="*60)
    archives_dir = OUTPUT_DIR / "Archives"
    clean_dir(archives_dir)
    win_src = OUTPUT_DIR / "Windows" / "RPT_YouTube_Portable"
    if win_src.exists():
        zip_path = archives_dir / f"RPT_YouTube_v{APP_VERSION}_Windows.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(win_src):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(win_src.parent)
                    zf.write(file_path, arcname)
        print(f"✅ Windows ZIP: {zip_path}")
    linux_src = OUTPUT_DIR / "Linux"
    if linux_src.exists():
        zip_path = archives_dir / f"RPT_YouTube_v{APP_VERSION}_Linux.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(linux_src):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(linux_src.parent)
                    zf.write(file_path, arcname)
        print(f"✅ Linux ZIP: {zip_path}")
    github_src = OUTPUT_DIR / "GitHub"
    if github_src.exists():
        zip_path = archives_dir / f"RPT_YouTube_v{APP_VERSION}_GitHub.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for root, dirs, files in os.walk(github_src):
                for file in files:
                    file_path = Path(root) / file
                    arcname = file_path.relative_to(github_src.parent)
                    zf.write(file_path, arcname)
        print(f"✅ GitHub ZIP: {zip_path}")
    return True

def print_summary():
    print("\n" + "="*60)
    print("✅ BUILD COMPLETE!")
    print("="*60)
    print(f"""
Output: {OUTPUT_DIR}
- Windows/RPT_YouTube_Portable/
- Linux/rpt-youtube_{APP_VERSION}_all.deb
- GitHub/
- Archives/
""")
    print("="*60)

def main():
    print("\n" + "="*60)
    print(f"RPT YouTube Export Tool v{APP_VERSION}")
    print("="*60)
    if not check_dependencies():
        print("\n⚠️ Please install missing dependencies and try again.")
        print("   pip install pyinstaller")
        return
    clean_dir(OUTPUT_DIR)
    win = build_windows_exe()
    lin = build_linux_deb()
    git = build_github_release()
    arch = create_archives()
    print_summary()
    if win:
        print("✅ Windows build successful!")
    else:
        print("⚠️ Windows build had issues.")
    if lin:
        print("✅ Linux build successful!")
    else:
        print("⚠️ Linux build had issues (dpkg-deb may not be available on Windows).")
    if git:
        print("✅ GitHub structure created!")
    print(f"\nOutput: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()