
import qrcode
import shutil
import secrets
import json
import os

# 1. Generate a unique code for ROI
roi_code = secrets.token_urlsafe(16)

# 2. Store the code in roi_token.json
with open('roi_token.json', 'w') as f:
    json.dump({'roi_token': roi_code}, f)

# Version production Render
base_url = "https://the-only-key.onrender.com"

# 4. Generate the QR code
url = f"{base_url}/auto_login?token={roi_code}"
img = qrcode.make(url)
img.save("roi_qr_prod.png")

# Ensure static directory exists
os.makedirs("static", exist_ok=True)
shutil.copy("roi_qr_prod.png", "static/roi_qr.png")

print("ROI code (PRODUCTION):", roi_code)
print("QR code saved for production")
print("URL:", url)
