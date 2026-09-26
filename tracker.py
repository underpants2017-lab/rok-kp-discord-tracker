import os
import requests
from bs4 import BeautifulSoup

WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
TARGET_URL = "https://prokingdoms.com/overview/stats/1841853"


def fetch_and_post():
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  try:
    response = requests.get(TARGET_URL, headers=headers, timeout=20)
    response.raise_for_status()
  except Exception as e:
    print(f"Error fetching page: {e}")
    return

  soup = BeautifulSoup(response.text, "html.parser")

  # Extract page title or player tag
  title = soup.title.string.strip() if soup.title else "Governor 1841853 Stats"

  # Construct the Discord Embed Payload
  payload = {
      "username": "ProKingdoms Intelligence",
      "avatar_url": "https://prokingdoms.com/favicon.ico",
      "embeds": [{
          "title": "⚔️ Daily KvK KP & Stats Report",
          "description": (
              f"**Governor Profile:** [ID 1841853]({TARGET_URL})\n**Dashboard"
              f" Overview:** `{title}`"
          ),
          "url": TARGET_URL,
          "color": 16766720,  # Gold
          "fields": [
              {
                  "name": "🎯 Target Tracked",
                  "value": "`1841853`",
                  "inline": True,
              },
              {
                  "name": "📊 Source Dashboard",
                  "value": "[ProKingdoms Stats](https://prokingdoms.com/)",
                  "inline": True,
              },
              {
                  "name": "🕒 Sync Timestamp",
                  "value": "Daily 00:00 UTC Reset",
                  "inline": False,
              },
          ],
          "footer": {
              "text": (
                  "ROK Tactical Command • Automatic Tracker • Zero-Cost"
                  " Automation"
              )
          },
      }],
  }

  res = requests.post(WEBHOOK_URL, json=payload)
  if res.status_code in (200, 204):
    print("Successfully posted to Discord!")
  else:
    print(f"Discord rejected payload with status code: {res.status_code}")


if __name__ == "__main__":
  fetch_and_post()
