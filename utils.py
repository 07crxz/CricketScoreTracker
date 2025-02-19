import requests
import time
from typing import Dict, Any


def send_discord_message(webhook_url: str, message: str, max_retries: int = 3) -> bool:
    embed = {
        "description": message,
        "color": 16711680 
    }

    payload = {
        "embeds": [embed]
    }    
    for attempt in range(max_retries):
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            if attempt == max_retries - 1:
                print(f"Failed to send Discord message after {max_retries} attempts: {str(e)}")
                return False
            time.sleep(1)
    
    return False

def format_score_message(match_info: Dict[Any, Any]) -> str:
    message = [
        "# Live Cricket Score Update",
        f"\n> **{match_info['title']}**",
        f"> *{match_info['status']}*\n"
    ]
    
    for team in match_info['teams']:
        message.append(f"> **{team['name']}**: {team['score']}")
    
    return "\n".join(message)
