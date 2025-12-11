"""AI Scheduler agent - Content publishing."""

from typing import Dict, Any, List, Optional
from datetime import datetime
import requests
from config import get_settings

settings = get_settings()


def schedule_post(
    content: Dict[str, Any],
    images: List[str],
    platform: str = "telegram",
    scheduled_time: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Schedule and publish content to platform.
    
    Args:
        content: Content dictionary
        images: List of image URLs
        platform: Target platform
        scheduled_time: Optional scheduled time
        
    Returns:
        Publishing result
    """
    try:
        if platform == "telegram":
            return _publish_telegram(content, images)
        elif platform == "vk":
            return _publish_vk(content, images)
        else:
            return {"success": False, "error": f"Platform {platform} not implemented"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _publish_telegram(content: Dict[str, Any], images: List[str]) -> Dict[str, Any]:
    """Publish to Telegram."""
    bot_token = settings.telegram_bot_token
    chat_id = settings.telegram_chat_id
    
    if not bot_token or not chat_id:
        return {"success": False, "error": "Telegram credentials not configured"}
    
    text = content.get("text", "")
    
    if images:
        # Send photo with caption
        url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        data = {
            "chat_id": chat_id,
            "caption": text,
            "photo": images[0]
        }
    else:
        # Send text only
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": text
        }
    
    response = requests.post(url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return {
            "success": True,
            "post_id": str(result.get("result", {}).get("message_id", "")),
            "platform": "telegram"
        }
    else:
        return {"success": False, "error": response.text}


def _publish_vk(content: Dict[str, Any], images: List[str]) -> Dict[str, Any]:
    """Publish to VK."""
    access_token = settings.vk_access_token
    group_id = settings.vk_group_id
    
    if not access_token or not group_id:
        return {"success": False, "error": "VK credentials not configured"}
    
    text = content.get("text", "")
    
    url = "https://api.vk.com/method/wall.post"
    params = {
        "owner_id": f"-{group_id}",
        "message": text,
        "access_token": access_token,
        "v": "5.131"
    }
    
    if images:
        params["attachments"] = ",".join(images)
    
    response = requests.post(url, params=params)
    result = response.json()
    
    if "response" in result:
        return {
            "success": True,
            "post_id": str(result["response"].get("post_id", "")),
            "platform": "vk"
        }
    else:
        return {"success": False, "error": result.get("error", {}).get("error_msg", "Unknown error")}

