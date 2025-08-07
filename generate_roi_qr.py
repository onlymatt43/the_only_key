import qrcode
import shutil
import secrets
import json

# 1. Generate a unique code for ROI
roi_code = secrets.token_urlsafe(16)

# 2. Store the code in roi_token.json
with open('roi_token.json', 'w') as f:
    json.dump({'roi_token': roi_code}, f)

# 3. Generate the QR code for local testing
url = f"http://localhost:10000/auto_login?token={roi_code}"
img = qrcode.make(url)
img.save("roi_qr.png")
shutil.copy("roi_qr.png", "static/roi_qr.png")

print("ROI code:", roi_code)
print("QR code saved as roi_qr.png")
print("URL:", url)
