# file: send.py
import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv


load_dotenv()
api_key = os.getenv("BREVO_API_KEY")


def send_newsletter(html_path: str, subject: str):
    # 1. Configure client
    cfg = sib_api_v3_sdk.Configuration()
    cfg.api_key['api-key'] = api_key
    api = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(cfg))

    # 2. Read the generated HTML/MD content
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 3. Fill message object
    email = sib_api_v3_sdk.SendSmtpEmail(
        sender={"email": "newsletter@turilabs.tech", "name": "Turi Labs"},
        to=[
            {"email": "", "name": "recp 1"}
        ],
        subject=subject,
        html_content=content,  # If you're sending markdown, you might want to convert it to HTML first
        headers={
            "List-Unsubscribe": "<mailto:unsubscribe@turilabs.tech>",
            "Precedence": "bulk",
            "X-Entity-Ref-ID": "newsletter-2025-04-19"
        },
        # Add these parameters
        reply_to={
            "email": "saiyashwanth@turilabs.tech",
            "name": "Turi Labs Founder"
        },
        # Optional tags for tracking
        tags=["newsletter", "daily-digest"]
    )

    # 4. Send and handle response
    try:
        response = api.send_transac_email(email)
        print(f"Email sent successfully! Response: {response}")
    except ApiException as e:
        print(f"Error sending email: {str(e)}")
        print(f"Error body: {e.body}")
        raise

if __name__ == "__main__":
    try:
        send_newsletter("newsletter/2025-04-23.md", "Here's what happened in the last 24 hours!")
    except Exception as e:
        print(f"Failed to send newsletter: {str(e)}")