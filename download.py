import logging
import re
import aiohttp
from tiktokapipy.async_api import AsyncTikTokAPI

async def download_tiktok(url: str) -> bytes | None:
    try:
        # Use navigation retries and timeout settings for better reliability
        async with AsyncTikTokAPI(navigation_retries=3, navigation_timeout=15) as api:
            video = await api.video(url)
            if not video:
                logging.error("Failed to get video info")
                return None
            
            # Get the download URL from the video object
            video_url = None
            if hasattr(video, 'video') and video.video:
                if hasattr(video.video, 'download_addr') and video.video.download_addr:
                    video_url = video.video.download_addr
                elif hasattr(video.video, 'play_addr') and video.video.play_addr:
                    video_url = video.video.play_addr
            
            if not video_url:
                logging.error("No video URL found in API response")
                return None
            
            # Use the API's context cookies to avoid 403 errors
            cookies = {}
            try:
                context_cookies = await api.context.cookies()
                cookies = {cookie["name"]: cookie["value"] for cookie in context_cookies if cookie["name"] == "tt_chain_token"}
            except Exception as e:
                logging.warning(f"Could not get cookies: {e}")
            
            # Download the video with proper headers and cookies
            async with aiohttp.ClientSession(cookies=cookies) as session:
                headers = {"referer": "https://www.tiktok.com/"}
                async with session.get(video_url, headers=headers) as resp:
                    if resp.status == 200:
                        logging.info(f"Video downloaded: {url}")
                        return await resp.read()
                    else:
                        logging.error(f"Download status {resp.status}")
    except Exception as e:
        logging.error(f"Error downloading video: {e}")
    return None