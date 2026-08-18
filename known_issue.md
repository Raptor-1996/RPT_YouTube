# Known Issues

## 🎬 Video Download Quality

### Issue Description
When downloading videos, the application successfully downloads the content but **defaults to 640p resolution** regardless of the quality selected in the interface.

### Current Behavior
- User selects: 1080p, 720p, 2160p, etc.
- Actual download: 640p (or lower)
- Audio download (MP3) works perfectly with selected quality

### Impact
**Affects:** Video downloads only (MP4, WEBM, MKV, AVI)  
**Not Affected:** Audio downloads (MP3) work correctly

### Workaround
1. After downloading, use third-party tools to upscale or convert
2. Use the audio download feature which works flawlessly
3. Download via `yt-dlp` directly from terminal as a temporary solution:
   ```bash
   yt-dlp -f "bestvideo[height<=1080]+bestaudio/best[height<=1080]" "YOUR_URL"
   '''