import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Optional

try:
    from twilio.rest import Client as TwilioClient
except Exception:
    TwilioClient = None  # Twilio optional


def send_email(
    smtp_host: str,
    smtp_port: int,
    username: str,
    password: str,
    sender: str,
    recipients: List[str],
    subject: str,
    html_body: str,
):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)

    part = MIMEText(html_body, 'html', 'utf-8')
    msg.attach(part)

    with smtplib.SMTP(smtp_host, smtp_port) as server:
        server.starttls()
        if username and password:
            server.login(username, password)
        server.sendmail(sender, recipients, msg.as_string())


def send_sms(
    account_sid: str,
    auth_token: str,
    from_number: str,
    to_numbers: List[str],
    body: str,
):
    if TwilioClient is None:
        raise RuntimeError("Twilio is not installed. Install 'twilio' package.")

    client = TwilioClient(account_sid, auth_token)
    for to_number in to_numbers:
        client.messages.create(from_=from_number, to=to_number, body=body)


