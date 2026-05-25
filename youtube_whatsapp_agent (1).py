# ============================================
#   YouTube → WhatsApp Notification Agent
#   Watches MN PRASAD channel & alerts you!
# ============================================
# Install dependencies first:
#   pip install requests twilio

import time
import json
import os
import requests
from twilio.rest import Client

# ── YOUR CREDENTIALS ─────────────────────────
RAPIDAPI_KEY     = "71bd0fda78mshca3d2687a2abbfap173e7cjsna7d5e64ee7bf"
RAPIDAPI_HOST    = "youtube-api49.p.rapidapi.com"
CHANNEL_ID       = "UC8w_HkQS4E2zfnwJH67XB4g"   # MN PRASAD

TWILIO_SID       = "AC0cb999c4e394ddc26ab6321d84433933"
TWILIO_TOKEN     = "66be05ecbcfaeb3f8fca787046c3f619"
TWILIO_WHATSAPP  = "whatsapp:+14155238886"        # Twilio sandbox number
MY_WHATSAPP      = "whatsapp:+916302345420"       # Your number

CHECK_INTERVAL   = 300   # Check every 5 minutes
STATE_FILE       = "last_video.json"
# ─────────────────────────────────────────────

def load_last_video():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f).get("video_id")
    return None

def save_last_video(video_id):
    with open(STATE_FILE, "w") as f:
        json.dump({"video_id": video_id}, f)

def get_latest_video():
    url = "https://youtube-api49.p.rapidapi.com/channel/videos"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {
        "channelId": CHANNEL_ID,
        "part": "snippet",
        "order": "date",
        "maxResults": "1"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    items = data.get("items", [])
    if not items:
        return None, None, None

    item     = items[0]
    video_id = item["id"]["videoId"]
    title    = item["snippet"]["title"]
    url      = f"https://youtube.com/watch?v={video_id}"
    return video_id, title, url

def send_whatsapp(title, url):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    msg = (
        "🎬 *New YouTube Video Alert!*\n\n"
        f"📺 *MN PRASAD* just uploaded:\n"
        f"*{title}*\n\n"
        f"🔗 {url}\n\n"
        "👆 Tap the link → Share as WhatsApp Status!"
    )
    client.messages.create(
        body=msg,
        from_=TWILIO_WHATSAPP,
        to=MY_WHATSAPP
    )
    print(f"✅ WhatsApp notification sent: {title}")

def run_agent():
    print("🤖 YouTube-WhatsApp Agent Started!")
    print(f"👀 Watching: MN PRASAD (UC8w_HkQS4E2zfnwJH67XB4g)")
    print(f"📱 Notifying: +916302345420")
    print(f"🔁 Checking every {CHECK_INTERVAL // 60} minutes\n")

    last_id = load_last_video()

    while True:
        try:
            print("🔍 Checking for new videos...")
            video_id, title, url = get_latest_video()

            if video_id and video_id != last_id:
                print(f"🆕 New video found: {title}")
                send_whatsapp(title, url)
                save_last_video(video_id)
                last_id = video_id
            else:
                print(f"⏳ No new video. Next check in {CHECK_INTERVAL // 60} minutes...")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_agent()
