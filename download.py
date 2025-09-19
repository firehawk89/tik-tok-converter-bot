import logging
import re
from TikTokApi import TikTokApi
from config import MS_TOKEN  

async def download_tiktok(url: str) -> bytes | None:
    try:
        async with TikTokApi(custom_verifyFp=MS_TOKEN) as api:
            video_id = extract_video_id(url)
            if not video_id:
                logging.error("Failed to extract video ID from URL")
                return None

            # Fetch the video object
            video = await api.video(id=video_id)
            if not video:
                logging.error("Failed to get video object")
                return None

            # Get raw video bytes
            video_bytes = await video.bytes()
            logging.info(f"Video downloaded: {url}")
            return video_bytes

    except Exception as e:
        logging.error(f"Error downloading video: {e}")
        return None


def extract_video_id(url: str) -> str | None:
    patterns = [
        r'tiktok\.com/@[^/]+/video/(\d+)',
        r'tiktok\.com/t/([a-zA-Z0-9]+)',
        r'vm\.tiktok\.com/([a-zA-Z0-9]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None
