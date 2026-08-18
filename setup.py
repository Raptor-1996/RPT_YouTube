from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="rpt-youtube",
    version="3.0.0",
    author="Raptor96",
    author_email="raptor96@example.com",
    description="YouTube Video & Audio Downloader with Modern GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Raptor-1996/RPT-YouTube",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "yt-dlp>=2023.12.30",
        "customtkinter>=5.2.0",
        "Pillow>=10.1.0",
        "pygame>=2.5.0",
    ],
    entry_points={
        "console_scripts": [
            "rpt-youtube=RPT_YouTube_v3:main",
        ],
    },
)