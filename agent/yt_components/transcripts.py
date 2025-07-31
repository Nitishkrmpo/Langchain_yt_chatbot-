import os
import re
import yt_dlp

import os
import yt_dlp
# from .utils import extract_video_id  # Assuming you have this utility
from pathlib import Path

def download_youtube_auto_subtitles(video_url: str, lang='en', output_dir="vtt_files") -> str:
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    ydl_opts = {
        'skip_download': True,
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': [lang],
        'subtitlesformat': 'vtt',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),  # Save in vtt_files directory
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=False)
        video_id = info.get("id")
        auto_caps = info.get("automatic_captions", {})
        sub_caps = info.get("subtitles", {})

        print(f"🔍 Auto-caption languages available: {list(auto_caps.keys())}")
        print(f"📝 Manual subtitles available: {list(sub_caps.keys())}")

        if lang not in auto_caps and lang not in sub_caps:
            raise Exception(f"❌ No subtitles found for language: {lang}")

        print("📥 Downloading subtitle file...")
        ydl.download([video_url])

        # Check for expected file in output directory
        expected_filename = os.path.join(output_dir, f"{video_id}.{lang}.vtt")
        if os.path.exists(expected_filename):
            return expected_filename
        else:
            # Fallback: look for any VTT file for this video in the output directory
            files = [f for f in os.listdir(output_dir) 
                     if f.endswith('.vtt') and f.startswith(video_id)]
            if files:
                return os.path.join(output_dir, files[0])
            raise FileNotFoundError(f"❌ VTT subtitle file not found in {output_dir} after download.")

import re
import os
from pathlib import Path

def parse_vtt_to_text(vtt_file_path: str) -> str:
    """Parse VTT file to clean text, preserving line breaks between subtitles"""
    try:
        # Read VTT file
        with open(vtt_file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remove headers and metadata
        content = re.sub(r'^WEBVTT.*\n?', '', content, flags=re.MULTILINE | re.IGNORECASE)
        content = re.sub(r'^Kind:.*\n?', '', content, flags=re.MULTILINE | re.IGNORECASE)
        content = re.sub(r'^Language:.*\n?', '', content, flags=re.MULTILINE | re.IGNORECASE)
        
        # Remove timestamps and position tags
        content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}.*\n', '', content)
        content = re.sub(r'align:start position:\d+%?', '', content)
        
        # Remove HTML tags
        content = re.sub(r'<[^>]+>', '', content)
        
        # Remove cue numbers
        content = re.sub(r'^\d+\n', '', content, flags=re.MULTILINE)
        
        # Process lines
        cleaned_lines = []
        for line in content.splitlines():
            line = line.strip()
            if line:
                # Preserve natural breaks between subtitles
                if not cleaned_lines or cleaned_lines[-1] != line:
                    cleaned_lines.append(line)
        
        # Join with spaces but preserve paragraph breaks
        return "\n\n".join(cleaned_lines)
    
    except Exception as e:
        raise RuntimeError(f"Error parsing VTT file: {str(e)}")
