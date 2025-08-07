import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# INSTRUCTIONS:
# 1. Set your Yahoo email and app password below.
# 2. Run this script: python3 send_roi_code_with_qr.py
# 3. The ROI code and QR image will be sent to om43@myyahoo.com

# Load the ROI code
with open('roi_token.json') as f:
    roi_code = json.load(f)['roi_token']

# Email details
sender = "om43@myyahoo.com"  # <-- SENDER
password = "aklgonbbkjxgjnts"         # <-- Yahoo app password
recipient = "onlymatt43@gmail.com"  # <-- RECIPIENT
subject = "Your ROI Admin Code"
body = f"Here is your ROI code: {roi_code}\n\nThe QR code image is attached."

# Create the email with attachment
msg = MIMEMultipart()
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = recipient
msg.attach(MIMEText(body, 'plain'))

# Attach the QR code image
filename = "roi_qr.png"
with open(filename, "rb") as attachment:
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    msg.attach(part)

# Send the email using Yahoo SMTP
with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
    server.login(sender, password)
    server.send_message(msg)

print("Email with QR code sent!")
