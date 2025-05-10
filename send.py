import os
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from datetime import datetime, timedelta
from dotenv import load_dotenv


# Get Brevo API key from environment (no .env file needed in GitHub Actions)
load_dotenv()
api_key = os.getenv("BREVO_API_KEY")

def send_newsletter(html_path: str, subject: str):
    if not api_key:
        print("Error: BREVO_API_KEY is not set in the environment")
        return False

    # 1. Configure client
    cfg = sib_api_v3_sdk.Configuration()
    cfg.api_key['api-key'] = api_key
    api = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(cfg))

    # 2. Read the generated HTML/MD content
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Newsletter file {html_path} not found")
        return False
    except Exception as e:
        print(f"Error reading newsletter file {html_path}: {str(e)}")
        return False

    # 3. Fill message object
    email = sib_api_v3_sdk.SendSmtpEmail(
        sender={"email": "newsletter@turilabs.tech", "name": "Turi Labs"},
        to=[
            {"email": "taddishetty24@gmail.com", "name": "rcp1"}
            # {"email": "iamsid0011@gmail.com", "name": "rcp2"},
            # {"email": "supratikkar2003@gmail.com", "name": "rcp3"},
            # {"email": "mayankrm2003@gmail.com", "name": "rcp4"},
            # {"email": "dhatri.c22@gmail.com", "name": "rcp5"}
        ],
        subject=subject,
        html_content=content,  # Consider converting Markdown to HTML if needed
        headers={
            "List-Unsubscribe": "<mailto:unsubscribe@turilabs.tech>",
            "Precedence": "bulk",
            "X-Entity-Ref-ID": f"newsletter-{datetime.now().strftime('%Y-%m-%d')}"
        },
        reply_to={
            "email": "saiyashwanth@turilabs.tech",
            "name": "Turi Labs Founder"
        },
        tags=["newsletter", "daily-digest"]
    )

    # 4. Send and handle response
    try:
        response = api.send_transac_email(email)
        print(f"Email sent successfully! Response: {response}")
        return True
    except ApiException as e:
        print(f"Error sending email: {str(e)}")
        print(f"Error body: {e.body}")
        return False
    except Exception as e:
        print(f"Unexpected error sending email: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        # Use dynamic date and correct path
        today = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d") 
        # today = "2025-03-10"
        newsletter_path = f"newsletter/{today}.md"
        subject = f"Here's what happened in the last 24 hours! ({today})"
        success = send_newsletter(newsletter_path, subject)
        if not success:
            print("Failed to send newsletter, but exiting with code 0 to avoid workflow failure")
            exit(0)  # Exit with 0 to avoid failing the workflow
    except Exception as e:
        print(f"Failed to send newsletter: {str(e)}")
        exit(0)  # Exit with 0 to avoid failing the workflow