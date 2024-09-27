from flask import Flask, request, render_template, send_file
import os
#from pytube import YouTube
import yt_dlp
import validators
import re
#import youtube_dl

app = Flask(__name__)

# Path to save downloaded files
DOWNLOAD_FOLDER = os.path.join(os.getcwd(), "downloads")
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to download video from YouTube
def download_youtube_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'verbose': True,  # Tambahkan ini untuk detail lebih lanjut
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            filepath = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp4")
            return filepath
    except Exception as e:
        print(f"Error downloading YouTube video: {e}")
        return None


# Function to download Instagram video using yt-dlp
def download_instagram_video(url):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'mp4',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.download([url])
            filepath = os.path.join(DOWNLOAD_FOLDER, ydl.prepare_filename(ydl.extract_info(url, download=False)))
            return filepath
    except Exception as e:
        print(f"Error downloading Instagram video: {e}")
        return None

# Function to download video from X/Twitter using yt-dlp
def download_twitter_video(url):
    ydl_opts = {
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
        'format': 'mp4',
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            info_dict = ydl.extract_info(url, download=False)
            video_title = info_dict.get('title', None)
            filepath = os.path.join(DOWNLOAD_FOLDER, f"{video_title}.mp4")
            return filepath
    except Exception as e:
        print(f"Error downloading Twitter video: {e}")
        return None

def is_valid_url(url):
    # Check if the URL is valid
    return validators.url(url)

# Function to check if URL is from a whitelisted domain
def is_valid_platform_url(url, platform):
    platform_whitelist = {
        'youtube': r'(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+',
        'instagram': r'(https?://)?(www\.)?instagram\.com/.+',
        'twitter': r'(https?://)?(www\.)?(x\.com|twitter\.com)/.+',
    }

    if platform in platform_whitelist:
        return re.match(platform_whitelist[platform], url)
    return False

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        video_url = request.form['url']
        platform = request.form['platform']

        # Validate URL
        if not is_valid_url(video_url) or not is_valid_platform_url(video_url, platform):
            return "Invalid URL. Please enter a valid URL."

        if platform == 'youtube':
            filepath = download_youtube_video(video_url)
        elif platform == 'instagram':
            filepath = download_instagram_video(video_url)
        elif platform == 'twitter':
            filepath = download_twitter_video(video_url)
        else:
            return "Platform not supported yet."

        if filepath:
            return send_file(filepath, as_attachment=True)
        else:
            return "Failed to download the video."

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)