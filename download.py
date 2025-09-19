import logging
import re
from TikTokApi import TikTokApi
from config import MS_TOKEN

async def download_tiktok(url: str) -> bytes | None:
    try:
        async with TikTokApi() as api:
            await api.create_sessions(
                ms_tokens=[MS_TOKEN] if MS_TOKEN else None, 
                num_sessions=1, 
                sleep_after=3
            )
            
            video_id = extract_video_id(url)
            if not video_id:
                logging.error("Failed to extract video ID from URL")
                return None
                
            video = await api.video(id=video_id).info()
            if not video:
                logging.error("Failed to get video info")
                return None
            
            video_url = None
            if hasattr(video, 'video') and video.video:
                # Check for playAddr (without watermark)
                if hasattr(video.video, 'playAddr') and video.video.playAddr:
                    video_url = video.video.playAddr

                elif hasattr(video.video, 'downloadAddr') and video.video.downloadAddr:
                    video_url = video.video.downloadAddr

                elif hasattr(video.video, 'playAddrLowBr') and video.video.playAddrLowBr:
                    video_url = video.video.playAddrLowBr
            
            if not video_url:
                logging.error("No video URL found in API response")
                return None
            
            # Use the API's session to download the video
            async with api.session_manager.session.get(video_url) as resp:
                if resp.status == 200:
                    logging.info(f"Video downloaded: {url}")
                    return await resp.read()
                else:
                    logging.error(f"Download status {resp.status}")
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
