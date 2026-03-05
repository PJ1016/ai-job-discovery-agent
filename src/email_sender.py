import os
import smtplib
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_job_email(report_html):
    """
    Sends the job discovery report via email.
    """
    email_user = os.getenv("EMAIL_USER")
    email_password = os.getenv("EMAIL_PASSWORD")
    receiver = os.getenv("EMAIL_RECEIVER")

    if not email_user or not email_password or not receiver:
        print("Error: Email configuration missing in .env")
        return False

    today = datetime.now().strftime("%B %d, %Y")
    
    msg = EmailMessage()
    msg["Subject"] = f"Daily AI Job Discovery Report - {today}"
    msg["From"] = email_user
    msg["To"] = receiver

    msg.add_alternative(report_html, subtype="html")

    try:
        print(f"Connecting to SMTP server to send report to {receiver}...")
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.send_message(msg)
        
        print("Email sent successfully!")
        return True

    except Exception as e:
        print(f"Email sending failed: {e}")
        return False
