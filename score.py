import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import os
from utils import send_discord_message, format_score_message

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1341692740915691520/Wpklknn6bDciBxqyBjyKy1Qn9IlNGEaDJALHnhFqMAKNSLPXxKb10zwwuJrCLdngCa4H"
FETCH_INTERVAL = 5 
MAX_RETRIES = 3

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_live_matches():
    try:
        print("Fetching live matches from Cricbuzz...")
        response = requests.get("https://www.cricbuzz.com/cricket-match/live-scores", headers=HEADERS)
        response.raise_for_status()
        print(f"Response status code: {response.status_code}")

        soup = BeautifulSoup(response.text, 'html.parser')
        live_matches = []
        
        match_cards = soup.find_all('div', class_='cb-mtch-lst')
        print(f"Found {len(match_cards)} match cards")

        for match in match_cards:
            try:
                title_elem = match.find('a', class_='text-hvr-underline')
                status_elem = (match.find('div', class_='cb-text-complete') or 
                             match.find('div', class_='cb-text-live') or
                             match.find('div', class_='cb-text-preview'))

                if not title_elem:
                    print("Missing title element, skipping...")
                    continue

                title = title_elem.text.strip()
                # if "Women" not in title:
                #     continue

                match_info = {
                    'title': title,
                    'status': status_elem.text.strip() if status_elem else "Status not available",
                    'teams': []
                }
                teams_container = (match.find('div', class_='cb-scr-wll-chvrn') or
                                 match.find('div', class_='cb-mtch-crd-state'))

                if teams_container:
                    team_elements = teams_container.find_all(['div', 'span'], 
                        class_=['cb-ovr-flo', 'cb-hmscg-tm-nm', 'cb-teams'])

                    current_team = {}
                    for elem in team_elements:
                        text = elem.text.strip()
                        if text:
                            if not current_team.get('name'):
                                current_team['name'] = text
                            else:
                                current_team['score'] = text
                                match_info['teams'].append(current_team)
                                current_team = {}

                if match_info['teams']:
                    print(f"Parsed WPL match: {match_info['title']}")
                    live_matches.append(match_info)
                else:
                    print(f"No team information found for WPL match: {match_info['title']}")

            except AttributeError as e:
                print(f"Error parsing match: {str(e)}")
                continue
            except Exception as e:
                print(f"Unexpected error parsing match: {str(e)}")
                continue

        return live_matches

    except requests.RequestException as e:
        print(f"Error fetching matches: {str(e)}")
        return None

def main():
    if not DISCORD_WEBHOOK_URL:
        print("webhook to de bkl")
        return

    print("Cricket Score Bot Started...")
    last_scores = {}

    while True:
        try:
            matches = get_live_matches()

            if matches:
                print(f"Processing {len(matches)} live matches")
                current_scores = {}

                for match in matches:
                    match_id = match['title'] 
                    current_scores[match_id] = match

                    if match_id not in last_scores or last_scores[match_id] != match:
                        print(f"Score update detected for: {match_id}")
                        message = format_score_message(match)
                        if send_discord_message(DISCORD_WEBHOOK_URL, message):
                            print("Successfully sent score update to Discord")
                        else:
                            print("Failed to send score update to Discord")

                last_scores = current_scores
            else:
                print("No live matches found")

            time.sleep(FETCH_INTERVAL)

        except Exception as e:
            print(f"Error in main loop: {str(e)}")
            time.sleep(FETCH_INTERVAL)
            continue

if __name__ == "__main__":
    main()
