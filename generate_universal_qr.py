import qrcode
import shutil
import os

# URL pour accès universel mobile
base_url = "https://the-only-key.onrender.com"
universal_url = f"{base_url}/mobile?unlock=universal"

# Génération du QR code universel
img = qrcode.make(universal_url)
img.save("universal_qr.png")

# S'assurer que le dossier static existe
os.makedirs("static", exist_ok=True)
shutil.copy("universal_qr.png", "static/universal_qr.png")

print("QR Code universel généré !")
print("URL:", universal_url)
print("Fichier sauvé: universal_qr.png et static/universal_qr.png")