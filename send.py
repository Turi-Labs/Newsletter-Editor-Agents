import os
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv(override=True)

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

def convert_md_to_slack(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Convert links
    for a in soup.find_all("a"):
        text = a.text.strip()
        href = a.get("href", "")
        a.replace_with(f"<{href}|{text}>")

    # Convert strong/bold
    for tag in soup.find_all(["strong", "b"]):
        tag.replace_with(f"*{tag.text.strip()}*")

    # Convert italic
    for tag in soup.find_all(["em", "i"]):
        tag.replace_with(f"_{tag.text.strip()}_")

    # Convert lists
    for li in soup.find_all("li"):
        li.replace_with(f"• {li.text.strip()}\n")

    # Convert paragraphs
    for p in soup.find_all("p"):
        p.replace_with(f"{p.text.strip()}\n\n")

    # Remove any remaining HTML tags
    text = soup.get_text()

    # Clean excess spacing
    lines = [line.rstrip() for line in text.split("\n")]
    return "\n".join([l for l in lines if l.strip() != ""])


def send_slack_message(md_path: str, title: str):
    if not SLACK_BOT_TOKEN:
        print("Error: SLACK_BOT_TOKEN is not set")
        return False
    if not CHANNEL_ID:
        print("Error: SLACK_CHANNEL_ID is not set")
        return False

    # Read markdown
    try:
        with open(md_path, "r", encoding="utf-8") as f:
            md_text = f.read()
    except Exception as e:
        print(f"Error reading md file: {str(e)}")
        return False

    # Convert MD → Slack formatting
    slack_text = convert_md_to_slack(md_text)

    # Slack API payload
    payload = {
        "channel": CHANNEL_ID,
        "text": f"*{title}*\n\n{slack_text}",
        "unfurl_links": False,
        "unfurl_media": False

    }

    # Send message
    response = requests.post(
        "https://slack.com/api/chat.postMessage",
        json=payload,
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        }
    )

    data = response.json()
    print("Slack Response:", data)

    return data.get("ok", False)


if __name__ == "__main__":
    try:
        today = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        md_path = f"newsletter/{today}.md"

        title = f"Daily Newsletter • {today}"

        success = send_slack_message(md_path, title)

        if not success:
            print("Slack message failed (but workflow won’t fail).")
            exit(0)

    except Exception as e:
        print("Unexpected error:", str(e))
        exit(0)
