"""
email_sender.py
Sends results or PDF via email.
"""

import smtplib
from email.message import EmailMessage

def send_email_with_attachment(to_email, subject, body, file_path):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = "no-reply@facilitatetheprocess.com"
    msg["To"] = to_email
    msg.set_content(body)

    with open(file_path, "rb") as f:
        file_data = f.read()
        file_name = file_path.split("/")[-1]
        msg.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

    with smtplib.SMTP("smtp.your-email-provider.com", 587) as smtp:
        smtp.starttls()
        smtp.login("your-username", "your-password")
        smtp.send_message(msg)
