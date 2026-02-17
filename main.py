from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Online", "message": "Queen Nelumi YouTube API is running!"}

@app.get("/api/download")
def download(url: str):
    if not url:
        raise HTTPException(status_code=400, detail="URL එකක් දීපම් රත්තරං!")

    # YouTube බ්ලොක් නොවී දත්ත ගන්න අවශ්‍ය Settings
    ydl_opts = {
        'format': 'best', # MP3 සහ MP4 දෙකටම හරියන හොඳම කොලිටිය
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'ios'], # මේකෙන් බ්ලොක් වෙන එක ගොඩක් අඩුවෙනවා
            }
        },
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # වීඩියෝ එකේ තොරතුරු Extract කිරීම
            info = ydl.extract_info(url, download=False)
            
            # Download URL එක සහ නම මෙතනින් ලැබෙනවා
            return {
                "status": "success",
                "title": info.get('title'),
                "download_url": info.get('url'),
                "thumbnail": info.get('thumbnail'),
                "duration": info.get('duration_string'),
                "author": info.get('uploader')
            }
    except Exception as e:
        # Error එකක් ආවොත් ඒක පෙන්වනවා
        raise HTTPException(status_code=500, detail=str(e))
