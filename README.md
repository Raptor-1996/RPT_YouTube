# 🎬 RPT YouTube

**YouTube Video & Audio Downloader** with modern GUI - Developed by Raptor96

[![GitHub license](https://img.shields.io/github/license/Raptor-1996/RPT-YouTube)](https://github.com/Raptor-1996/RPT_YouTube/blob/main/LICENSE)
[![GitHub release](https://img.shields.io/github/v/release/Raptor-1996/RPT-YouTube)](https://github.com/Raptor-1996/RPT_YouTube/releases)
[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)](https://github.com/Raptor-1996/RPT_YouTube)

---

## ✨ Features

- 📥 **Video Download** - 144p to 2160p (MP4, WEBM, MKV, AVI)
- 🎵 **Audio Download** - MP3 64-320 kbps
- 🌙 **Dark/Light Themes** - Easy on the eyes
- 🌍 **Bilingual** - English & Persian support
- 📊 **Real-time Progress** - Speed, ETA, percentage
- 📁 **Auto Organization** - Videos & Musics folders
- 📜 **Download History** - Track your downloads
- ⚙️ **Custom Settings** - Save your preferences

---

## 🚀 Quick Start

### Windows
1. Download the latest `RPT_YouTube.exe` from [Releases](https://github.com/Raptor-1996/RPT-YouTube/releases)
2. Run the executable (no installation required!)

### Linux
1. Download the `.deb` package from [Releases](https://github.com/Raptor-1996/RPT-YouTube/releases)
2. Install with: `sudo dpkg -i rpt-youtube_*.deb`
3. Run: `rpt-youtube`

### From Source

# Clone the repository
```
git clone https://github.com/Raptor-1996/RPT-YouTube.git
cd RPT-YouTube
```

# Install dependencies
```
pip install -r requirements.txt
```

# Run the application
```
python RPT_YouTube_v3.py
```

📦 Requirements
```
Python 3.7+

FFmpeg (required for audio download & conversion)

Dependencies (auto-installed on first run):

yt-dlp - YouTube downloading

customtkinter - Modern GUI

Pillow - Image processing

pygame - Sound notifications
```

FFmpeg Installation
Windows:

powershell
# Using Chocolatey

```
choco install ffmpeg
```

# Using Winget
```
winget install ffmpeg
```

# Or download manually from https://ffmpeg.org/download.html
Linux:

```
bash
sudo apt install ffmpeg        # Ubuntu/Debian
sudo dnf install ffmpeg        # Fedora
sudo pacman -S ffmpeg          # Arch
```

🛠️ Building from Source
The project includes Export_Proj.py for creating distribution packages:

bash
```
python Export_Proj.py
```
This will generate:
```
Windows portable EXE

Linux DEB package

GitHub release structure
```
ZIP archives

Manual Build (Windows)
```bash
pip install pyinstaller
python -m PyInstaller --onefile --windowed --name "RPT_YouTube" --icon assets/icon.ico --add-data "assets;assets" RPT_YouTube_v3.py
```

🎯 Usage Guide
Paste a YouTube URL into the input field

Click "Check" to fetch video information

Choose your download type (Video/Audio)

Select format & quality

Pick your save location

Click "Download" and watch the progress!

🗂️ Project Structure
text
RPT-YouTube/
├── RPT_YouTube_v3.py      # Main application
├── Export_Proj.py         # Build & packaging script
├── assets/
│   ├── icon.ico          # Windows icon
│   ├── icon.png          # Application icon
│   ├── success.mp3       # Success sound
│   ├── found.mp3         # Found sound
│   └── failed.mp3        # Error sound
├── requirements.txt      # Python dependencies
├── README.md             # This file
├── LICENSE               # MIT License
└── .gitignore           # Git ignore file
🤝 Contributing
Fork the repository

Create a feature branch (git checkout -b feature/amazing)

Commit your changes (git commit -m 'Add amazing feature')

Push to the branch (git push origin feature/amazing)

Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

👨‍💻 Developer
Raptor96

GitHub: @Raptor-1996

Project: RPT-YouTube

⭐ Support
If you like this project, please consider:

⭐ Starring the repository

🐛 Reporting issues

💡 Suggesting features

Made with ❤️ by Raptor96
