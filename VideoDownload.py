import eel
import yt_dlp
import os
import threading
import sys
from bs4 import BeautifulSoup

os.chdir(os.path.dirname(__file__))

# Create downloads folder
os.makedirs("downloads", exist_ok=True)

# Initialize Eel (frontend in 'setting' folder)
eel.init("setting")

# Track download progress
progress_data = {"status": "", "percent": 0, "speed": 0}

last_download_info = None

@eel.expose
def get_last_download():
    return last_download_info

# Path to home HTML where recent downloads will be added
home_html = "Content.html"

@eel.expose
def add_to_home(title, filepath, thumbnail):
    home_html = "Content.html"
    new_block = f'''
    <a href="{filepath}">
        <img src="{thumbnail}" width="120">
        <label>{title}</label>
    </a>
    '''
    with open(home_html, "r", encoding="utf-8") as f:
        html = f.read()
    if filepath in html:
        return
    html = html.replace("</line>", new_block + "</line>")
    with open(home_html, "w", encoding="utf-8") as f:
        f.write(html)

def download_video(url, resolution):
    global progress_data

    def progress_hook(d):
        global progress_data, last_download_info

        if d['status'] == 'downloading':
            progress_data["status"] = "Downloading"
            progress_data["percent"] = round(d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100, 1)
            progress_data["speed"] = d.get('speed', 0)

        elif d['status'] == 'finished':
            progress_data["status"] = "Completed"
            progress_data["percent"] = 100
            progress_data["speed"] = 0

            info = d.get("info_dict", {})
            title = info.get("title", "Unknown")

            # final merged file path
            filepath = info.get("requested_downloads", [{}])[0].get("filepath")
            if not filepath or not os.path.exists(filepath):
                filepath = os.path.join("downloads", f"{title}.mp4")

            thumbnail = os.path.splitext(filepath)[0] + ".webp"
            if not os.path.exists(thumbnail):
                thumbnail = ""

            last_download_info = {"title": title, "filepath": filepath, "thumbnail": thumbnail}

    # yt-dlp options
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best[height<={resolution}]',
        'merge_output_format': 'mp4',
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'writethumbnail': True,
        'noplaylist': True,
        'concurrent_fragment_downloads': 5,
        'fragment_retries': 5,
        'quiet': True,
        'progress_hooks': [progress_hook],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@eel.expose
def start_download(url, resolution):
    global progress_data, last_download_info
    # Reset progress at the start
    progress_data = {"status": "Downloading", "percent": 0, "speed": 0}
    last_download_info = None
    threading.Thread(target=download_video, args=(url, resolution)).start()

@eel.expose
def get_progress():
    return progress_data

# Start Eel GUI
eel.start("videoDownload.html", mode="default")
