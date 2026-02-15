from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "message": "Welcome to YT Downloader API"}

@app.get("/api/download")
def download_video(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL එකක් අවශ්‍යයි")
    
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            return {
                "title": info.get('title'),
                "thumbnail": info.get('thumbnail'),
                "download_url": info.get('url'),
                "duration": info.get('duration_string'),
                "uploader": info.get('uploader')
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

