"""
RPT YouTube - Complete Final Version
YouTube Video & Audio Downloader with Modern GUI
Developer: Raptor96
GitHub: https://github.com/Raptor-1996/
"""

import os
import sys
import json
import re
import threading
import time
import subprocess
import shutil
import urllib.request
import io
import importlib
import tkinter as tk
from pathlib import Path
from datetime import datetime
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk

# =============================================
# DEPENDENCY CHECKER
# =============================================

class DependencyChecker:
    """Check and install required dependencies"""
    
    REQUIRED_PACKAGES = {
        'yt_dlp': 'yt-dlp',
        'customtkinter': 'customtkinter',
        'PIL': 'Pillow',
        'pygame': 'pygame'
    }
    
    @staticmethod
    def check_package(package_name):
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False
    
    @staticmethod
    def install_package(package_name):
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", package_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            return True
        except:
            return False
    
    @staticmethod
    def check_ffmpeg():
        ffmpeg_path = shutil.which('ffmpeg')
        if ffmpeg_path:
            return True
        common_paths = [
            'C:\\ffmpeg\\bin\\ffmpeg.exe',
            'C:\\Program Files\\ffmpeg\\bin\\ffmpeg.exe',
            os.path.expanduser('~\\ffmpeg\\bin\\ffmpeg.exe'),
        ]
        for path in common_paths:
            if os.path.exists(path):
                bin_dir = os.path.dirname(path)
                os.environ['PATH'] = bin_dir + os.pathsep + os.environ['PATH']
                return True
        return False
    
    @staticmethod
    def check_all_dependencies():
        status = {}
        for import_name, pip_name in DependencyChecker.REQUIRED_PACKAGES.items():
            status[pip_name] = DependencyChecker.check_package(import_name)
        status['ffmpeg'] = DependencyChecker.check_ffmpeg()
        return status
    
    @staticmethod
    def install_missing_dependencies():
        missing = []
        for import_name, pip_name in DependencyChecker.REQUIRED_PACKAGES.items():
            if not DependencyChecker.check_package(import_name):
                missing.append(pip_name)
        success_count = 0
        failed_packages = []
        for package in missing:
            if DependencyChecker.install_package(package):
                success_count += 1
            else:
                failed_packages.append(package)
        return success_count, failed_packages
    
    @staticmethod
    def install_ffmpeg_windows():
        try:
            print("📦 Attempting to install FFmpeg...")
            try:
                subprocess.run(['choco', '--version'], capture_output=True, check=True)
                print("✅ Chocolatey found, installing ffmpeg...")
                subprocess.run(['choco', 'install', 'ffmpeg', '-y'], check=True)
                return True
            except:
                pass
            try:
                subprocess.run(['winget', '--version'], capture_output=True, check=True)
                print("✅ Winget found, installing ffmpeg...")
                subprocess.run(['winget', 'install', 'ffmpeg'], check=True)
                return True
            except:
                pass
            print("❌ Could not install FFmpeg automatically")
            return False
        except Exception as e:
            print(f"❌ FFmpeg installation failed: {e}")
            return False


# =============================================
# TRANSLATOR
# =============================================

class Translator:
    """Multi-language translation"""
    
    def __init__(self, language='english'):
        self.language = language
        self.translations = {
            'english': {
                'app_title': 'RPT YouTube',
                'enter_url': 'Enter YouTube URL:',
                'check': 'Check',
                'validating': 'Validating...',
                'video_info': 'Video Information',
                'title': 'Title:',
                'channel': 'Channel:',
                'date': 'Date:',
                'download_type': 'Download Type:',
                'video': 'Video',
                'audio': 'Audio',
                'format': 'Format:',
                'quality': 'Quality:',
                'save_location': 'Save Location:',
                'browse': 'Browse',
                'download': 'Download',
                'downloading': 'Downloading...',
                'speed': 'Speed:',
                'progress': 'Progress:',
                'downloaded': 'Downloaded:',
                'remaining': 'Remaining:',
                'eta': 'ETA:',
                'settings': 'Settings',
                'language_label': 'Language:',
                'theme_label': 'Theme:',
                'dark': 'Dark',
                'light': 'Light',
                'save_path': 'Download Path:',
                'success': 'Download completed successfully!',
                'failed': 'Download failed!',
                'invalid_url': 'Invalid URL or video is private!',
                'found': 'Video information found!',
                'unable_to_reach': 'Unable to reach video: {}',
                'ready': 'Ready',
                'cancel': 'Cancel',
                'choose_language': 'Please choose your language:',
                'english': 'English',
                'persian': 'Persian',
                'first_run': 'Welcome to RPT YouTube!',
                'history': 'Download History',
                'select_folder': 'Select Folder',
                'select_download_path': 'Please select a valid download path',
                'ffmpeg_missing': 'FFmpeg is not installed. Audio downloads may not work.'
            },
            'persian': {
                'app_title': 'آرپی‌تی یوتیوب',
                'enter_url': 'لینک یوتیوب را وارد کنید:',
                'check': 'بررسی',
                'validating': 'در حال بررسی...',
                'video_info': 'اطلاعات ویدئو',
                'title': 'عنوان:',
                'channel': 'کانال:',
                'date': 'تاریخ:',
                'download_type': 'نوع دانلود:',
                'video': 'ویدئو',
                'audio': 'صوتی',
                'format': 'فرمت:',
                'quality': 'کیفیت:',
                'save_location': 'محل ذخیره‌سازی:',
                'browse': 'انتخاب',
                'download': 'دانلود',
                'downloading': 'در حال دانلود...',
                'speed': 'سرعت:',
                'progress': 'پیشرفت:',
                'downloaded': 'دانلود شده:',
                'remaining': 'باقی‌مانده:',
                'eta': 'زمان باقی‌مانده:',
                'settings': 'تنظیمات',
                'language_label': 'زبان:',
                'theme_label': 'تم:',
                'dark': 'تاریک',
                'light': 'روشن',
                'save_path': 'مسیر ذخیره‌سازی:',
                'success': 'دانلود با موفقیت انجام شد!',
                'failed': 'دانلود ناموفق بود!',
                'invalid_url': 'لینک نامعتبر است یا ویدئو خصوصی می‌باشد!',
                'found': 'اطلاعات ویدئو پیدا شد!',
                'unable_to_reach': 'عدم دسترسی به ویدئو: {}',
                'ready': 'آماده',
                'cancel': 'انصراف',
                'choose_language': 'لطفاً زبان خود را انتخاب کنید:',
                'english': 'انگلیسی',
                'persian': 'فارسی',
                'first_run': 'به آرپی‌تی یوتیوب خوش آمدید!',
                'history': 'تاریخچه دانلود',
                'select_folder': 'انتخاب پوشه',
                'select_download_path': 'لطفاً یک مسیر معتبر انتخاب کنید',
                'ffmpeg_missing': 'اف‌اف‌مپگ نصب نیست. دانلود صوتی ممکن است کار نکند.'
            }
        }
    
    def get(self, key):
        return self.translations.get(self.language, self.translations['english']).get(key, key)
    
    def set_language(self, language):
        if language in self.translations:
            self.language = language
            return True
        return False


# =============================================
# CONFIG MANAGER
# =============================================

class ConfigManager:
    """Manage application settings"""
    
    def __init__(self):
        self.config_dir = Path.home() / "RPT_YouTube"
        self.config_file = self.config_dir / "config.json"
        self.config_dir.mkdir(exist_ok=True)
        self.default_config = {
            "language": "english",
            "theme": "dark",
            "download_path": str(Path.home() / "Downloads")
        }
        self.config = self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return self.default_config.copy()
        return self.default_config.copy()
    
    def save_config(self):
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except:
            return False
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()
    
    def get_download_path(self):
        path = self.get('download_path')
        if path and os.path.exists(path):
            return path
        return str(Path.home() / "Downloads")
    
    def get_language(self):
        return self.get('language', 'english')
    
    def get_theme(self):
        return self.get('theme', 'dark')


# =============================================
# HISTORY MANAGER
# =============================================

class HistoryManager:
    """Manage download history"""
    
    def __init__(self):
        self.history_file = Path.home() / "RPT_YouTube" / "list.txt"
        if not self.history_file.exists():
            self.history_file.parent.mkdir(exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                f.write("=== RPT YouTube Download History ===\n")
                f.write("Title | Date | Time | Format | Quality\n")
                f.write("-" * 60 + "\n")
    
    def add_download(self, title, format_type, quality):
        now = datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")
        try:
            with open(self.history_file, 'a', encoding='utf-8') as f:
                f.write(f"{title} | {date} | {time} | {format_type} | {quality}\n")
            return True
        except:
            return False


# =============================================
# VIDEO INFO
# =============================================

class VideoInfo:
    """Get video information from YouTube"""
    
    def __init__(self):
        self.ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
            'ignoreerrors': True,
            'no_check_certificate': True,
            'headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            }
        }
    
    def get_info(self, url):
        try:
            from yt_dlp import YoutubeDL
            with YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                if info is None:
                    return None
                video_info = {
                    'title': info.get('title', 'Unknown Title'),
                    'channel': info.get('uploader', 'Unknown Channel'),
                    'date': info.get('upload_date', 'Unknown Date'),
                    'thumbnail': info.get('thumbnail', ''),
                    'duration': info.get('duration', 0),
                    'views': info.get('view_count', 0),
                    'url': url
                }
                if video_info['date'] != 'Unknown Date' and len(video_info['date']) == 8:
                    video_info['date'] = f"{video_info['date'][0:4]}-{video_info['date'][4:6]}-{video_info['date'][6:8]}"
                return video_info
        except Exception as e:
            print(f"Video info error: {e}")
            return None


# =============================================
# DOWNLOADER - FINAL FIXED FOR AUDIO & VIDEO
# =============================================

class Downloader:
    """Download management with proper audio and video support"""
    
    def __init__(self, callback=None):
        self.callback = callback
        self.is_downloading = False
        self.last_progress = 0
    
    def download(self, url, format_type, quality, output_path):
        if self.is_downloading:
            return False
        
        # Create subfolder based on type
        if format_type == 'mp3':
            output_path = os.path.join(output_path, 'Musics')
        else:
            output_path = os.path.join(output_path, 'Videos')
        
        # Create folder if not exists
        os.makedirs(output_path, exist_ok=True)
        
        self.is_downloading = True
        thread = threading.Thread(target=self._download_thread, args=(url, format_type, quality, output_path))
        thread.daemon = True
        thread.start()
        return True
    
    def _download_thread(self, url, format_type, quality, output_path):
        try:
            from yt_dlp import YoutubeDL
            
            output_template = os.path.join(output_path, '%(title)s.%(ext)s')
            
            # ===== BASE OPTIONS =====
            ydl_opts = {
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self._progress_hook],
                'ignoreerrors': True,
                'no_check_certificate': True,
                'prefer_insecure': True,
                'force_ipv4': True,
                'retries': 30,
                'fragment_retries': 30,
                'socket_timeout': 60,
                'extract_flat': False,
                'cookiesfrombrowser': ('chrome',),
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['dash', 'hls'],
                        'player_skip': ['configs', 'webpage'],
                    }
                },
                'compat_opts': ['no-live-chat'],
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept-Encoding': 'gzip, deflate, br',
                    'DNT': '1',
                    'Connection': 'keep-alive',
                    'Upgrade-Insecure-Requests': '1',
                },
            }
            
            # ===== AUDIO DOWNLOAD (MP3) =====
            if format_type == 'mp3':
                # Extract quality number (e.g., "128 kbps" -> "128")
                quality_num = quality.split()[0] if ' ' in quality else '128'
                
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality_num,
                    }],
                    'extractaudio': True,
                    'audioformat': 'mp3',
                    # Keep original file after conversion
                    'keepvideo': False,
                })
                print(f"🎵 Downloading AUDIO as MP3 (quality: {quality})")
                
            # ===== VIDEO DOWNLOAD =====
            else:
                quality_map = {
                    '2160p': 2160,
                    '1440p': 1440,
                    '1080p': 1080,
                    '720p': 720,
                    '480p': 480,
                    '360p': 360,
                    '240p': 240,
                    '144p': 144
                }
                target_height = quality_map.get(quality, 720)
                ydl_opts['format'] = f'bestvideo[height<={target_height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={target_height}][ext=mp4]/best'
                ydl_opts['merge_output_format'] = 'mp4'
                print(f"🎬 Downloading VIDEO (quality: {quality})")
            
            print(f"📥 Starting download...")
            print(f"   URL: {url}")
            print(f"   Format: {format_type}")
            print(f"   Quality: {quality}")
            print(f"   Output: {output_path}")
            
            with YoutubeDL(ydl_opts) as ydl:
                # First get info to show title
                info = ydl.extract_info(url, download=False)
                if info:
                    print(f"📋 Found: {info.get('title', 'Unknown')}")
                # Then download
                ydl.download([url])
            
            print(f"✅ Download completed successfully!")
            self.is_downloading = False
            if self.callback:
                self.callback('success', {'message': 'Download completed!'})
                
        except Exception as e:
            self.is_downloading = False
            error_msg = str(e)
            print(f"❌ Download error: {error_msg}")
            
            # If cookies fail, try without cookies
            if 'cookies' in error_msg.lower() or '403' in error_msg:
                print("🔄 Retrying without cookies...")
                self._download_no_cookies(url, format_type, quality, output_path)
            else:
                if self.callback:
                    self.callback('error', {'message': error_msg})
    
    def _download_no_cookies(self, url, format_type, quality, output_path):
        """Fallback download without cookies"""
        try:
            from yt_dlp import YoutubeDL
            
            output_template = os.path.join(output_path, '%(title)s.%(ext)s')
            
            quality_map = {
                '2160p': 2160, '1440p': 1440, '1080p': 1080,
                '720p': 720, '480p': 480, '360p': 360,
                '240p': 240, '144p': 144
            }
            target_height = quality_map.get(quality, 720)
            
            ydl_opts = {
                'outtmpl': output_template,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self._progress_hook],
                'ignoreerrors': True,
                'no_check_certificate': True,
                'prefer_insecure': True,
                'force_ipv4': True,
                'retries': 30,
                'fragment_retries': 30,
                'socket_timeout': 60,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web'],
                        'skip': ['dash', 'hls'],
                    }
                },
                'headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                },
            }
            
            # Audio
            if format_type == 'mp3':
                quality_num = quality.split()[0] if ' ' in quality else '128'
                ydl_opts.update({
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': quality_num,
                    }],
                    'extractaudio': True,
                    'audioformat': 'mp3',
                })
                print(f"🎵 Downloading AUDIO as MP3 (no cookies)...")
            else:
                ydl_opts['format'] = f'bestvideo[height<={target_height}][ext=mp4]+bestaudio[ext=m4a]/best[height<={target_height}][ext=mp4]/best'
                ydl_opts['merge_output_format'] = 'mp4'
                print(f"🎬 Downloading VIDEO (no cookies)...")
            
            print("🔄 Downloading without cookies...")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            self.is_downloading = False
            if self.callback:
                self.callback('success', {'message': 'Download completed!'})
                
        except Exception as e:
            self.is_downloading = False
            print(f"❌ Fallback failed: {e}")
            if self.callback:
                self.callback('error', {'message': str(e)})
    
    def _progress_hook(self, d):
        """Progress hook with proper formatting"""
        if d['status'] == 'downloading':
            percent_str = d.get('_percent_str', '0%').strip()
            if percent_str.endswith('%'):
                percent_str = percent_str[:-1]
            
            try:
                percent = float(percent_str)
            except:
                percent = 0
            
            progress_data = {
                'status': 'downloading',
                'percent': percent,
                'percent_str': f"{percent:.1f}%",
                'speed': d.get('_speed_str', '0').strip(),
                'downloaded': d.get('_downloaded_str', '0').strip(),
                'total': d.get('_total_bytes_str', '0').strip(),
                'eta': d.get('_eta_str', '--').strip()
            }
            
            if self.callback:
                self.callback('progress', progress_data)
                
        elif d['status'] == 'finished':
            if self.callback:
                self.callback('finished', {'message': 'Processing...'})
# =============================================
# SPLASH SCREEN
# =============================================

class SplashScreen:
    """Simple splash screen"""
    
    def __init__(self, callback=None):
        self.root = ctk.CTk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        
        self.width = 600
        self.height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - self.width) // 2
        y = (screen_height - self.height) // 2
        self.root.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.root.configure(fg_color='#1a1a1a')
        
        self.callback = callback
        self.is_finished = False
        self.progress_value = 0
        
        self.build_ui()
        self.animate_progress()
        self.root.after(3000, self.finish_splash)
    
    def build_ui(self):
        main_frame = ctk.CTkFrame(self.root, fg_color='#1a1a1a', corner_radius=0)
        main_frame.pack(fill='both', expand=True)
        
        title = ctk.CTkLabel(main_frame, text="RPT YouTube", 
                            font=('Segoe UI', 52, 'bold'), text_color='#ff3333')
        title.pack(pady=(80, 5))
        
        subtitle = ctk.CTkLabel(main_frame, text="YouTube Downloader",
                               font=('Segoe UI', 18), text_color='#888888')
        subtitle.pack()
        
        creator = ctk.CTkLabel(main_frame, text="by Raptor96",
                              font=('Segoe UI', 12), text_color='#555555')
        creator.pack(pady=(5, 20))
        
        self.loading_text = ctk.CTkLabel(main_frame, text="Loading...",
                                        font=('Segoe UI', 13), text_color='#666666')
        self.loading_text.pack(pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(main_frame, width=400, height=8,
                                              progress_color='#ff3333', corner_radius=4)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
    
    def animate_progress(self):
        if self.is_finished:
            return
        if self.progress_value < 100:
            self.progress_value += 1
            self.progress_bar.set(self.progress_value / 100)
            if self.progress_value < 30:
                text = "Loading..."
            elif self.progress_value < 60:
                text = "Initializing..."
            elif self.progress_value < 85:
                text = "Preparing..."
            else:
                text = "Almost ready..."
            self.loading_text.configure(text=text)
            self.root.after(25, self.animate_progress)
    
    def finish_splash(self):
        if self.is_finished:
            return
        self.is_finished = True
        self.loading_text.configure(text="Starting application...")
        self.progress_bar.set(1.0)
        self.root.after(100, self._close_and_start)
    
    def _close_and_start(self):
        self.root.destroy()
        if self.callback:
            self.callback()
    
    def run(self):
        self.root.mainloop()


# =============================================
# SETTINGS PANEL
# =============================================

class SettingsPanel:
    """Settings dialog"""
    
    def __init__(self, parent, config_manager, translator):
        self.parent = parent
        self.config = config_manager
        self.translator = translator
        
        self.window = ctk.CTkToplevel(parent)
        self.window.title(self.translator.get('settings'))
        self.window.geometry("500x380")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.window.iconbitmap(icon_path)
        except:
            pass
        
        self.build_ui()
        self.load_settings()
    
    def build_ui(self):
        main_frame = ctk.CTkFrame(self.window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Language
        lang_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        lang_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(lang_frame, text=self.translator.get('language_label'), 
                    font=('Segoe UI', 14)).pack(anchor="w", padx=5, pady=5)
        self.lang_var = ctk.StringVar(value="english")
        lang_menu = ctk.CTkOptionMenu(lang_frame, values=["english", "persian"],
                                     variable=self.lang_var, font=('Segoe UI', 12), width=200)
        lang_menu.pack(anchor="w", padx=5)
        
        # Theme
        theme_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        theme_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(theme_frame, text=self.translator.get('theme_label'),
                    font=('Segoe UI', 14)).pack(anchor="w", padx=5, pady=5)
        self.theme_var = ctk.StringVar(value="dark")
        theme_menu = ctk.CTkOptionMenu(theme_frame, values=["dark", "light"],
                                      variable=self.theme_var, font=('Segoe UI', 12), width=200)
        theme_menu.pack(anchor="w", padx=5)
        
        # Download Path
        path_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        path_frame.pack(fill="x", pady=10)
        ctk.CTkLabel(path_frame, text=self.translator.get('save_path'),
                    font=('Segoe UI', 14)).pack(anchor="w", padx=5, pady=5)
        path_input_frame = ctk.CTkFrame(path_frame, fg_color="transparent")
        path_input_frame.pack(fill="x", padx=5)
        self.path_var = ctk.StringVar()
        path_entry = ctk.CTkEntry(path_input_frame, textvariable=self.path_var,
                                 font=('Segoe UI', 12), width=350)
        path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        browse_btn = ctk.CTkButton(path_input_frame, text="...", command=self.browse_path,
                                  font=('Segoe UI', 12), width=40)
        browse_btn.pack(side="right")
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(side="bottom", fill="x", pady=20)
        save_btn = ctk.CTkButton(button_frame, text=self.translator.get('download'),
                                command=self.save_settings, font=('Segoe UI', 14, 'bold'),
                                fg_color="#00cc66", hover_color="#00994d", height=40)
        save_btn.pack(side="left", padx=5, fill="x", expand=True)
        cancel_btn = ctk.CTkButton(button_frame, text=self.translator.get('cancel'),
                                  command=self.window.destroy, font=('Segoe UI', 14),
                                  fg_color="#666666", hover_color="#444444", height=40)
        cancel_btn.pack(side="right", padx=5, fill="x", expand=True)
    
    def load_settings(self):
        self.lang_var.set(self.config.get_language())
        self.theme_var.set(self.config.get_theme())
        self.path_var.set(self.config.get_download_path())
    
    def browse_path(self):
        path = filedialog.askdirectory(title=self.translator.get('select_folder'))
        if path:
            self.path_var.set(path)
    
    def save_settings(self):
        path = self.path_var.get()
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except:
                messagebox.showerror("Error", "Invalid path selected!")
                return
        self.config.set('language', self.lang_var.get())
        self.config.set('theme', self.theme_var.get())
        self.config.set('download_path', path)
        ctk.set_appearance_mode(self.theme_var.get())
        self.translator.set_language(self.lang_var.get())
        messagebox.showinfo("Success", "Settings saved successfully!")
        self.window.destroy()


# =============================================
# MAIN WINDOW
# =============================================

class MainWindow:
    """Main application window"""
    
    def __init__(self, config_manager=None):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.root = ctk.CTk()
        self.root.title("RPT YouTube")
        self.root.geometry("1280x720")
        self.root.minsize(900, 600)
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.ico')
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except:
            pass
        
        self.config = config_manager or ConfigManager()
        self.translator = Translator(self.config.get_language())
        self.video_info = VideoInfo()
        self.downloader = None
        self.history = HistoryManager()
        self.video_data = None
        self.is_downloading = False
        self.progress_labels = {}
        self.current_format = 'mp4'
        
        self.apply_theme()
        self.build_ui()
        self.load_settings()
    
    def apply_theme(self):
        theme = self.config.get_theme()
        ctk.set_appearance_mode("light" if theme == 'light' else "dark")
    
    def build_ui(self):
        # Main container
        self.main_frame = ctk.CTkScrollableFrame(self.root, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        self.create_header()
        
        # URL Section
        self.create_url_section()
        
        # Video info (hidden)
        self.video_info_frame = ctk.CTkFrame(self.main_frame)
        self.video_info_frame.pack(fill="x", padx=10, pady=10)
        self.video_info_frame.pack_forget()
        
        # Download settings (hidden)
        self.download_settings_frame = ctk.CTkFrame(self.main_frame)
        self.download_settings_frame.pack(fill="x", padx=10, pady=10)
        self.download_settings_frame.pack_forget()
        
        # Progress (hidden)
        self.progress_frame = ctk.CTkFrame(self.main_frame)
        self.progress_frame.pack(fill="x", padx=10, pady=10)
        self.progress_frame.pack_forget()
        
        # Status bar
        self.create_status_bar()
        
        # Settings button
        self.create_settings_button()
    
    def create_header(self):
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(0, 20))
        
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.pack(side="left")
        
        try:
            icon_path = os.path.join(os.path.dirname(__file__), 'assets', 'icon.png')
            if os.path.exists(icon_path):
                img = Image.open(icon_path)
                img = img.resize((40, 40), Image.Resampling.LANCZOS)
                icon = ctk.CTkImage(img, size=(40, 40))
                icon_label = ctk.CTkLabel(title_frame, image=icon, text="")
                icon_label.pack(side="left", padx=(0, 10))
        except:
            pass
        
        title_label = ctk.CTkLabel(title_frame, text=self.translator.get('app_title'),
                                  font=('Segoe UI', 24, 'bold'))
        title_label.pack(side="left")
        
        version_label = ctk.CTkLabel(header_frame, text="v2.0.0",
                                    font=('Segoe UI', 12), text_color="gray")
        version_label.pack(side="right", padx=(0, 10))
    
    def create_url_section(self):
        url_frame = ctk.CTkFrame(self.main_frame)
        url_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        label = ctk.CTkLabel(url_frame, text=self.translator.get('enter_url'),
                            font=('Segoe UI', 14))
        label.pack(anchor="w", padx=10, pady=(10, 5))
        
        input_frame = ctk.CTkFrame(url_frame, fg_color="transparent")
        input_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.url_entry = ctk.CTkEntry(input_frame, 
                                     placeholder_text="https://www.youtube.com/watch?v=...",
                                     font=('Segoe UI', 14), 
                                     height=45)
        self.url_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Enable right-click paste menu
        self.url_entry.bind("<Button-3>", self._show_paste_menu)
        self.url_entry.bind("<Control-v>", self._paste_from_clipboard)
        self.url_entry.bind("<Command-v>", self._paste_from_clipboard)
        
        self.check_button = ctk.CTkButton(input_frame, text=self.translator.get('check'),
                                         command=self.check_video, height=45,
                                         font=('Segoe UI', 14, 'bold'),
                                         fg_color="#ff3333", hover_color="#cc0000")
        self.check_button.pack(side="right")
    
    def _show_paste_menu(self, event):
        """Show right-click context menu with paste option"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Paste", command=self._paste_from_clipboard)
        menu.add_command(label="Clear", command=lambda: self.url_entry.delete(0, tk.END))
        menu.add_separator()
        menu.add_command(label="Select All", command=lambda: self.url_entry.select_range(0, tk.END))
        try:
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            menu.grab_release()
    
    def _paste_from_clipboard(self, event=None):
        """Paste from clipboard into entry"""
        try:
            clipboard_text = self.root.clipboard_get()
            if clipboard_text:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, clipboard_text)
        except:
            pass
    
    def create_video_info_panel(self):
        for widget in self.video_info_frame.winfo_children():
            widget.destroy()
        
        title_label = ctk.CTkLabel(self.video_info_frame, text=self.translator.get('video_info'),
                                  font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        content_frame = ctk.CTkFrame(self.video_info_frame, fg_color="transparent")
        content_frame.pack(fill="x", padx=10, pady=5)
        
        thumb_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        thumb_frame.pack(side="left", padx=(0, 20))
        
        try:
            if self.video_data and self.video_data.get('thumbnail'):
                thumb_url = self.video_data['thumbnail']
                with urllib.request.urlopen(thumb_url) as response:
                    img_data = response.read()
                    img = Image.open(io.BytesIO(img_data))
                    img = img.resize((320, 180), Image.Resampling.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    thumb_label = ctk.CTkLabel(thumb_frame, image=photo, text="")
                    thumb_label.image = photo
                    thumb_label.pack()
        except:
            fallback_label = ctk.CTkLabel(thumb_frame, text="🎬", font=('Segoe UI', 60))
            fallback_label.pack()
        
        details_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        details_frame.pack(side="left", fill="both", expand=True)
        
        title_text = self.video_data.get('title', 'Unknown') if self.video_data else 'Unknown'
        ctk.CTkLabel(details_frame, text=f"{self.translator.get('title')} {title_text}",
                    font=('Segoe UI', 14, 'bold'), wraplength=500, justify="left").pack(anchor="w", pady=2)
        
        channel_text = self.video_data.get('channel', 'Unknown') if self.video_data else 'Unknown'
        ctk.CTkLabel(details_frame, text=f"{self.translator.get('channel')} {channel_text}",
                    font=('Segoe UI', 12), wraplength=500, justify="left").pack(anchor="w", pady=2)
        
        date_text = self.video_data.get('date', 'Unknown') if self.video_data else 'Unknown'
        ctk.CTkLabel(details_frame, text=f"{self.translator.get('date')} {date_text}",
                    font=('Segoe UI', 12), wraplength=500, justify="left").pack(anchor="w", pady=2)
        
        self.video_info_frame.pack(fill="x", padx=10, pady=10)
    
    def create_download_settings(self):
        for widget in self.download_settings_frame.winfo_children():
            widget.destroy()
        
        # Download type
        type_frame = ctk.CTkFrame(self.download_settings_frame, fg_color="transparent")
        type_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(type_frame, text=f"{self.translator.get('download_type')} ",
                    font=('Segoe UI', 14)).pack(side="left")
        
        self.download_type_var = ctk.StringVar(value="video")
        ctk.CTkRadioButton(type_frame, text=self.translator.get('video'),
                          variable=self.download_type_var, value="video",
                          command=self.on_download_type_change,
                          font=('Segoe UI', 12)).pack(side="left", padx=(20, 10))
        ctk.CTkRadioButton(type_frame, text=self.translator.get('audio'),
                          variable=self.download_type_var, value="audio",
                          command=self.on_download_type_change,
                          font=('Segoe UI', 12)).pack(side="left", padx=10)
        
        # Format
        format_frame = ctk.CTkFrame(self.download_settings_frame, fg_color="transparent")
        format_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(format_frame, text=f"{self.translator.get('format')} ",
                    font=('Segoe UI', 14)).pack(side="left")
        self.format_var = ctk.StringVar()
        self.format_menu = ctk.CTkOptionMenu(format_frame, values=["MP4"],
                                            variable=self.format_var,
                                            font=('Segoe UI', 12), width=150)
        self.format_menu.pack(side="left", padx=(20, 10))
        
        # Quality
        quality_frame = ctk.CTkFrame(self.download_settings_frame, fg_color="transparent")
        quality_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(quality_frame, text=f"{self.translator.get('quality')} ",
                    font=('Segoe UI', 14)).pack(side="left")
        self.quality_var = ctk.StringVar()
        self.quality_menu = ctk.CTkOptionMenu(quality_frame, values=["1080p"],
                                             variable=self.quality_var,
                                             font=('Segoe UI', 12), width=150)
        self.quality_menu.pack(side="left", padx=(20, 10))
        
        self.on_download_type_change()
        
        # Save location
        path_frame = ctk.CTkFrame(self.download_settings_frame, fg_color="transparent")
        path_frame.pack(fill="x", padx=10, pady=5)
        ctk.CTkLabel(path_frame, text=f"{self.translator.get('save_location')} ",
                    font=('Segoe UI', 14)).pack(side="left")
        self.path_var = ctk.StringVar(value=self.config.get_download_path())
        path_entry = ctk.CTkEntry(path_frame, textvariable=self.path_var,
                                 font=('Segoe UI', 12), width=400)
        path_entry.pack(side="left", padx=(20, 10), fill="x", expand=True)
        ctk.CTkButton(path_frame, text=self.translator.get('browse'),
                     command=self.browse_path, font=('Segoe UI', 12),
                     width=100).pack(side="right", padx=(0, 10))
        
        # Download button
        download_frame = ctk.CTkFrame(self.download_settings_frame, fg_color="transparent")
        download_frame.pack(fill="x", padx=10, pady=(10, 20))
        self.download_button = ctk.CTkButton(download_frame, text=self.translator.get('download'),
                                            command=self.start_download,
                                            font=('Segoe UI', 14, 'bold'), height=45,
                                            fg_color="#00cc66", hover_color="#00994d")
        self.download_button.pack(pady=10)
        
        self.download_settings_frame.pack(fill="x", padx=10, pady=10)
    
    def on_download_type_change(self):
        is_audio = self.download_type_var.get() == "audio"
        if is_audio:
            self.format_menu.configure(values=["MP3"])
            self.format_var.set("MP3")
            qualities = ["320 kbps", "256 kbps", "192 kbps", "128 kbps", "64 kbps"]
            self.quality_menu.configure(values=qualities)
            self.quality_var.set("128 kbps")
            self.current_format = 'mp3'
        else:
            self.format_menu.configure(values=["MP4", "WEBM", "MKV", "AVI"])
            self.format_var.set("MP4")
            qualities = ["2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"]
            self.quality_menu.configure(values=qualities)
            self.quality_var.set("720p")
            self.current_format = 'mp4'
    
    def check_video(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Warning", "Please enter a YouTube URL")
            return
        
        self.check_button.configure(state="disabled", text=self.translator.get('validating'))
        thread = threading.Thread(target=self._check_video_thread, args=(url,))
        thread.daemon = True
        thread.start()
    
    def _check_video_thread(self, url):
        try:
            info = self.video_info.get_info(url)
            if info:
                self.video_data = info
                self.root.after(0, self._show_video_info)
                self.play_sound('found')
                self.root.after(0, self._show_download_settings)
            else:
                self.root.after(0, self._show_error, self.translator.get('invalid_url'))
                self.play_sound('failed')
        except Exception as e:
            error_msg = self.translator.get('unable_to_reach').format(str(e))
            self.root.after(0, self._show_error, error_msg)
            self.play_sound('failed')
        finally:
            self.root.after(0, self._enable_check_button)
    
    def _show_video_info(self):
        self.create_video_info_panel()
    
    def _show_download_settings(self):
        self.create_download_settings()
    
    def _show_error(self, message):
        messagebox.showerror("Error", message)
    
    def _enable_check_button(self):
        self.check_button.configure(state="normal", text=self.translator.get('check'))
    
    def browse_path(self):
        path = filedialog.askdirectory(title=self.translator.get('select_folder'))
        if path:
            self.path_var.set(path)
            self.config.set('download_path', path)
    
    def start_download(self):
        if self.is_downloading:
            return
        if not self.video_data:
            messagebox.showwarning("Warning", "Please check a video first")
            return
        
        url = self.video_data.get('url')
        format_type = self.format_var.get().lower()
        quality = self.quality_var.get()
        output_path = self.path_var.get()
        
        if not output_path or not os.path.exists(output_path):
            messagebox.showwarning("Warning", self.translator.get('select_download_path'))
            return
        
        self.show_progress_panel()
        self.is_downloading = True
        self.download_button.configure(state="disabled", text=self.translator.get('downloading'))
        
        self.downloader = Downloader(callback=self.download_callback)
        thread = threading.Thread(target=self.downloader.download,
                                 args=(url, format_type, quality, output_path))
        thread.daemon = True
        thread.start()
    
    def show_progress_panel(self):
        for widget in self.progress_frame.winfo_children():
            widget.destroy()
        
        title_label = ctk.CTkLabel(self.progress_frame, text=self.translator.get('downloading'),
                                  font=('Segoe UI', 16, 'bold'))
        title_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=600, height=20,
                                              progress_color="#ff3333", border_width=2, corner_radius=10)
        self.progress_bar.pack(padx=10, pady=10)
        self.progress_bar.set(0)
        
        info_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=5)
        
        self.progress_labels['speed'] = ctk.CTkLabel(info_frame, text=f"{self.translator.get('speed')} --",
                                                    font=('Segoe UI', 12))
        self.progress_labels['speed'].pack(side="left", padx=(0, 20))
        
        self.progress_labels['percent'] = ctk.CTkLabel(info_frame, text=f"{self.translator.get('progress')} 0%",
                                                      font=('Segoe UI', 12))
        self.progress_labels['percent'].pack(side="left", padx=(0, 20))
        
        self.progress_labels['downloaded'] = ctk.CTkLabel(info_frame, text=f"{self.translator.get('downloaded')} 0 MB",
                                                         font=('Segoe UI', 12))
        self.progress_labels['downloaded'].pack(side="left", padx=(0, 20))
        
        self.progress_labels['remaining'] = ctk.CTkLabel(info_frame, text=f"{self.translator.get('remaining')} 0 MB",
                                                        font=('Segoe UI', 12))
        self.progress_labels['remaining'].pack(side="left", padx=(0, 20))
        
        self.progress_labels['eta'] = ctk.CTkLabel(info_frame, text=f"{self.translator.get('eta')} --",
                                                  font=('Segoe UI', 12))
        self.progress_labels['eta'].pack(side="left")
        
        self.progress_frame.pack(fill="x", padx=10, pady=10)
    
    def download_callback(self, status, data):
        if status == 'progress':
            self.root.after(0, self._update_progress, data)
        elif status == 'finished':
            self.root.after(0, self._download_finished, True)
        elif status == 'success':
            self.root.after(0, self._download_complete)
            self.play_sound('success')
        elif status == 'error':
            self.root.after(0, self._download_finished, False, data.get('message'))
            self.play_sound('failed')
    
    def _update_progress(self, data):
        try:
            # Update progress bar
            percent = data.get('percent', 0)
            self.progress_bar.set(percent / 100)
            
            # Update labels with proper formatting
            self.progress_labels['speed'].configure(
                text=f"{self.translator.get('speed')} {data.get('speed', '--')}"
            )
            self.progress_labels['percent'].configure(
                text=f"{self.translator.get('progress')} {data.get('percent_str', '0%')}"
            )
            self.progress_labels['downloaded'].configure(
                text=f"{self.translator.get('downloaded')} {data.get('downloaded', '0')}"
            )
            self.progress_labels['remaining'].configure(
                text=f"{self.translator.get('remaining')} {data.get('total', '0')}"
            )
            self.progress_labels['eta'].configure(
                text=f"{self.translator.get('eta')} {data.get('eta', '--')}"
            )
        except Exception as e:
            print(f"Progress update error: {e}")
    
    def _download_complete(self):
        if self.video_data:
            title = self.video_data.get('title', 'Unknown')
            format_type = self.format_var.get()
            quality = self.quality_var.get()
            self.history.add_download(title, format_type, quality)
        messagebox.showinfo("Success", self.translator.get('success'))
        self._reset_download_state()
    
    def _download_finished(self, success, error_msg=None):
        if not success and error_msg:
            messagebox.showerror("Error", error_msg)
        self._reset_download_state()
    
    def _reset_download_state(self):
        self.is_downloading = False
        self.download_button.configure(state="normal", text=self.translator.get('download'))
        self.progress_frame.pack_forget()
    
    def play_sound(self, sound_type):
        try:
            import pygame
            sound_file = os.path.join(os.path.dirname(__file__), 'assets', f'{sound_type}.mp3')
            if os.path.exists(sound_file):
                pygame.mixer.init()
                pygame.mixer.music.load(sound_file)
                pygame.mixer.music.play()
        except:
            pass
    
    def load_settings(self):
        lang = self.config.get_language()
        self.translator.set_language(lang)
    
    def create_status_bar(self):
        status_frame = ctk.CTkFrame(self.root, height=30)
        status_frame.pack(side="bottom", fill="x")
        status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(status_frame, text=self.translator.get('ready'),
                                        font=('Segoe UI', 11))
        self.status_label.pack(side="left", padx=10)
        
        lang_indicator = ctk.CTkLabel(status_frame, text=self.config.get_language().upper(),
                                     font=('Segoe UI', 11, 'bold'))
        lang_indicator.pack(side="right", padx=10)
    
    def create_settings_button(self):
        settings_frame = ctk.CTkFrame(self.root, fg_color="transparent", height=40)
        settings_frame.pack(side="top", fill="x", padx=10, pady=(5, 0))
        settings_frame.pack_propagate(False)
        
        settings_btn = ctk.CTkButton(settings_frame, text="⚙️ " + self.translator.get('settings'),
                                    command=self.open_settings, font=('Segoe UI', 12),
                                    width=100, height=30)
        settings_btn.pack(side="right", padx=5)
    
    def open_settings(self):
        settings = SettingsPanel(self.root, self.config, self.translator)
        settings.window.mainloop()
    
    def run(self):
        self.root.mainloop()


# =============================================
# MAIN APPLICATION
# =============================================

class RPTYouTubeApp:
    """Main application class"""
    
    def __init__(self):
        self.config_dir = Path.home() / "RPT_YouTube"
        self.config_dir.mkdir(exist_ok=True)
        self.config = ConfigManager()
        self.is_first_run = not self.config.config_file.exists()
        
        if not self.check_dependencies():
            return
        
        self.show_splash()
    
    def check_dependencies(self):
        status = DependencyChecker.check_all_dependencies()
        
        packages_installed = all(status.get(pkg, False) for pkg in ['yt-dlp', 'customtkinter', 'Pillow', 'pygame'])
        
        if not packages_installed:
            missing = [pkg for pkg, installed in status.items() if pkg != 'ffmpeg' and not installed]
            msg = "Missing dependencies:\n\n"
            for pkg in missing:
                msg += f"• {pkg}\n"
            msg += "\nDo you want to install them automatically?"
            
            root = ctk.CTk()
            root.withdraw()
            response = messagebox.askyesno("Missing Dependencies", msg, parent=root)
            root.destroy()
            
            if response:
                success_count, failed = DependencyChecker.install_missing_dependencies()
                if failed:
                    messagebox.showerror("Installation Failed",
                        f"Failed to install: {', '.join(failed)}\n\nPlease install them manually.")
                    return False
            else:
                return False
        
        if not status.get('ffmpeg', False):
            response = messagebox.askyesno("FFmpeg Required",
                "FFmpeg is not installed.\n\nVideo downloads work, but audio conversion may fail.\n\n"
                "Do you want to install FFmpeg automatically?")
            if response:
                if DependencyChecker.install_ffmpeg_windows():
                    messagebox.showinfo("Success", "FFmpeg installed successfully!")
                else:
                    messagebox.showwarning("FFmpeg Warning",
                        "Could not install FFmpeg automatically.\nPlease install manually from:\n"
                        "https://ffmpeg.org/download.html")
        
        return True
    
    def show_splash(self):
        splash = SplashScreen(callback=self.start_main_app)
        splash.run()
    
    def start_main_app(self):
        try:
            main_window = MainWindow(self.config)
            main_window.run()
        except Exception as e:
            root = ctk.CTk()
            root.withdraw()
            messagebox.showerror("Error", f"Failed to start application: {e}")
            root.destroy()


# =============================================
# ENTRY POINT
# =============================================

if __name__ == "__main__":
    app = RPTYouTubeApp()