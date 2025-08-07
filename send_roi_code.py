import smtplib
import json
from email.mime.text import MIMEText

# Load the ROI code
with open('roi_token.json') as f:
    roi_code = json.load(f)['roi_token']

# Email details
sender = "your_email@gmail.com"  # Change to your email
password = "your_app_password"   # Change to your app password
recipient = "om43@myyahoo.com"
subject = "Your ROI Admin Code"
body = f"Here is your ROI code: {roi_code}"

# Create the email
msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = sender
msg['To'] = recipient

# Send the email
with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
    server.login(sender, password)
    server.send_message(msg)

print("Email sent!")
