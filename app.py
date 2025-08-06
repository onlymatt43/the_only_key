
from flask import Flask, render_template, request, redirect, make_response, jsonify
import os
import json
import time
import secrets
import hashlib
from collections import defaultdict
import logging
from functools import wraps

app = Flask(__name__)

# Route d'auto-login universelle depuis l'index
@app.route('/auto_login')
def auto_login():
    token = request.args.get('token', '').strip()
    if not token:
        return redirect('/')
    roi_token = get_roi_token() or ':roi'
    cleanup_tokens()
    # Si token roi
    if token == roi_token or token == ':roi':
        return redirect(f'/roi_login?token={token}')
    # Si token admin
    if token in token_store:
        # On peut raffiner ici si tu veux distinguer admin/user par un champ dans le store
        # Pour l'instant, on considère tout token valide comme admin si demandé
        # (ou tu peux ajouter une logique pour différencier)
        # Si tu veux une vraie distinction, il faut stocker le rôle dans token_store
        return redirect(f'/admin_login?token={token}')
    # Sinon, on tente user
    return redirect(f'/user_login?token={token}')

# --- Routes d'auto-login par QR code pour chaque rôle ---
from flask import Flask, render_template, request, redirect, make_response, jsonify
import os
import json
import time
import secrets
import hashlib
from collections import defaultdict
import logging
from functools import wraps

app = Flask(__name__)

# --- Routes d'auto-login par QR code pour chaque rôle ---
@app.route('/roi_login')
def roi_login():
    token = request.args.get('token', '').strip()
    roi_token = get_roi_token() or ':roi'
    if token == roi_token:
        resp = make_response(redirect('/admin_qr'))
        # Authentifie comme admin ET roi
        resp.set_cookie('admin_auth', ADMIN_PASSWORD, max_age=3600, httponly=True, secure=True)
        resp.set_cookie('access_token', roi_token, max_age=3600, httponly=True, secure=True)
        return resp
    return "Token roi invalide", 403

@app.route('/admin_login')
def admin_login():
    token = request.args.get('token', '').strip()
    # Vérifie que le token existe dans le store
    cleanup_tokens()
    if token in token_store:
        # Authentifie comme admin (accès limité)
        resp = make_response(redirect('/admin_qr'))
        resp.set_cookie('admin_auth', ADMIN_PASSWORD, max_age=3600, httponly=True, secure=True)
        resp.set_cookie('access_token', token, max_age=3600, httponly=True, secure=True)
        return resp
    return "Token admin invalide", 403

@app.route('/user_login')
def user_login():
    token = request.args.get('token', '').strip()
    cleanup_tokens()
    if token in token_store:
        # Authentifie comme user (accès page sécurisée)
        page = token_store[token].get('page', 'page_unlock')
        resp = make_response(redirect('/unlocked'))
        resp.set_cookie('access_token', token, max_age=3600, httponly=True, secure=True)
        resp.set_cookie('page_to_unlock', page, max_age=3600, httponly=True, secure=True)
        return resp
    return "Token user invalide", 403

# --- Anti-bruteforce et logs d'accès ---
ACCESS_LOG = "access.log"
attempts_per_ip = defaultdict(list)  # {ip: [timestamps]}
MAX_ATTEMPTS = 10
WINDOW_SECONDS = 300  # 5 minutes
def log_access(ip, token, status, user_agent):
    with open(ACCESS_LOG, "a") as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | IP: {ip} | Token: {token} | Status: {status} | UA: {user_agent}\n")

# --- Protection admin par mot de passe simple ---
ADMIN_PASSWORD = "adminpass"  # À changer !
def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if request.cookies.get("admin_auth") == ADMIN_PASSWORD:
            return f(*args, **kwargs)
        if request.method == "POST":
            if request.form.get("admin_password") == ADMIN_PASSWORD:
                resp = make_response(redirect(request.path))
                resp.set_cookie("admin_auth", ADMIN_PASSWORD, max_age=3600, httponly=True, secure=True)
                return resp
        return render_template("admin_login.html")
    return decorated

# Gestion du token roi unique (persistant)
ROI_FILE = "roi_token.json"
def get_roi_token():
    if os.path.exists(ROI_FILE):
        with open(ROI_FILE, "r") as f:
            data = json.load(f)
            return data.get("roi")
    return None

def set_roi_token(token):
    # Ne permet de définir le roi qu'une seule fois, jamais de reset ni de transfert
    if os.path.exists(ROI_FILE):
        return  # Figer le roi pour toujours
    with open(ROI_FILE, "w") as f:
        json.dump({"roi": token}, f)

@app.route('/gen_token_hash', methods=['POST'])
def gen_token_hash():
    original = secrets.token_urlsafe(16)
    hashed = hashlib.sha256(original.encode()).hexdigest()
    expires_at = time.time() + 3600
    token_store[hashed] = {"expires_at": expires_at}
    save_token_store()
    return {"token": hashed}

TOKEN_FILE = "token_store.json"

if os.path.exists(TOKEN_FILE):
    with open(TOKEN_FILE, "r") as f:
        token_store = json.load(f)
else:
    token_store = {}

# Nettoyer les tokens expirés
def cleanup_tokens():
    now = time.time()
    expired = [t for t, v in token_store.items() if v["expires_at"] < now]
    for t in expired:
        del token_store[t]
    if expired:
        save_token_store()

def save_token_store():
    with open(TOKEN_FILE, "w") as f:
        json.dump(token_store, f)

def is_mobile():
    ua = request.headers.get('User-Agent', '').lower()
    return "iphone" in ua or "android" in ua

@app.route('/')
def home():
    return render_template('index.html')

# Route pour générer un token de test (simple, non sécurisé)
@app.route('/generate_token', methods=['POST'])
def generate_token():
    # Optionnel: ajouter un mot de passe simple en paramètre POST
    password = request.form.get('password', '')
    if password != 'testpass':
        return "Accès refusé", 403
    token = secrets.token_urlsafe(16)
    expires_at = time.time() + 3600  # 1h
    token_store[token] = {"expires_at": expires_at}
    save_token_store()
    cleanup_tokens()
    return {"token": token, "expires_at": expires_at}

@app.route('/mobile', methods=['GET', 'POST'])
def unlock_mobile():
    if not is_mobile():
        return render_template("mobile_only.html")

    if request.method == 'POST':
        ip = request.remote_addr
        now = time.time()
        # Nettoie les anciennes tentatives
        attempts_per_ip[ip] = [t for t in attempts_per_ip[ip] if now-t < WINDOW_SECONDS]
        if len(attempts_per_ip[ip]) >= MAX_ATTEMPTS:
            log_access(ip, 'N/A', 'blocked', request.headers.get('User-Agent',''))
            return render_template("unlock_mobile.html", error="Trop de tentatives. Réessayez plus tard.")
        attempts_per_ip[ip].append(now)
        raw = request.form.get("token", "").strip()
        cleanup_tokens()
        # Format attendu: TOKEN:5m:page ou TOKEN:2h:page ou TOKEN:30s:page ou TOKEN:1d:page
        # ou TOKEN:5m ou TOKEN:2h (compatibilité)
        page = 'page_unlock'
        if ':' in raw:
            parts = raw.split(':')
            if len(parts) == 3:
                token, duration_str, page = parts
            elif len(parts) == 2:
                token, duration_str = parts
                page = 'page_unlock'
            else:
                token = raw
                duration_str = ''
            duration_str = duration_str.strip().lower()
            if duration_str.endswith('s'):
                duree = int(duration_str[:-1])
            elif duration_str.endswith('m'):
                duree = int(duration_str[:-1]) * 60
            elif duration_str.endswith('h'):
                duree = int(duration_str[:-1]) * 3600
            elif duration_str.endswith('d'):
                duree = int(duration_str[:-1]) * 86400
            else:
                duree = 3600  # défaut 1h
        else:
            token = raw
            duree = 3600
            page = 'page_unlock'
        # Gestion du QR roi dynamique : le premier admin à utiliser :roi devient le roi
        roi_token = get_roi_token()
        if token == ':roi':
            if not is_mobile():
                log_access(ip, token, 'fail-not-mobile', request.headers.get('User-Agent',''))
                return render_template("mobile_only.html")
            if roi_token is None:
                set_roi_token(':roi')
                roi_token = ':roi'
            if token == roi_token:
                log_access(ip, token, 'success-roi', request.headers.get('User-Agent',''))
                resp = make_response(redirect('/unlocked'))
                resp.set_cookie("access_token", roi_token, httponly=True, secure=True)
                resp.set_cookie("page_to_unlock", page, httponly=True, secure=True)
                return resp
            else:
                log_access(ip, token, 'fail-roi', request.headers.get('User-Agent',''))
                return render_template("unlock_mobile.html", error=True)
        elif token in token_store:
            user_ip = request.remote_addr
            device_id = request.cookies.get('device_id')
            if 'ip' not in token_store[token] and 'device_id' not in token_store[token]:
                token_store[token]['ip'] = user_ip
                token_store[token]['device_id'] = device_id
                token_store[token]['expires_at'] = time.time() + duree
                token_store[token]['page'] = page
                save_token_store()
            log_access(ip, token, 'success', request.headers.get('User-Agent',''))
            resp = make_response(redirect('/unlocked'))
            resp.set_cookie("access_token", token, max_age=duree, httponly=True, secure=True)
            resp.set_cookie("page_to_unlock", page, max_age=duree, httponly=True, secure=True)
            return resp
        else:
            log_access(ip, raw, 'fail', request.headers.get('User-Agent',''))
            return render_template("unlock_mobile.html", error=True)
    return render_template("unlock_mobile.html", error=False)

@app.route('/unlocked')
def unlocked():
    token = request.cookies.get("access_token")
    device_id = request.cookies.get("device_id")
    user_ip = request.remote_addr
    cleanup_tokens()
    page = request.cookies.get("page_to_unlock", "page_unlock")
    roi_token = get_roi_token()
    if token == roi_token:
        # Accès illimité pour le roi, mais uniquement depuis un mobile
        if not is_mobile():
            return render_template("mobile_only.html")
        return render_template(f"{page}.html")
    if token and token in token_store:
        t = token_store[token]
        # Vérifie l'expiration, l'IP et le device_id
        if (
            time.time() < t.get("expires_at", 0)
            and t.get("ip") == user_ip
            and t.get("device_id") == device_id
        ):
            page = t.get('page', page)
            return render_template(f"{page}.html")
        else:
            return redirect('/expired')
    return redirect('/mobile')

@app.route('/expired')
def expired():
    return render_template("time_up.html")

@app.route('/play')
def play_game():
    return render_template("play_game.html")


# Page admin pour générer des QR codes personnalisés
@app.route('/admin_qr', methods=["GET", "POST"])
@admin_required
def admin_qr():
    # QR code universel permanent qui pointe vers /universal_qr
    base_url = request.url_root.rstrip('/')
    universal_qr_url = f"{base_url}/universal_qr"
    # QR roi (pour compatibilité)
    roi_token = get_roi_token() or ':roi'
    qr_code = f"{roi_token}:permanent:page_unlock"
    return render_template("admin_qr.html", qr_code_roi=qr_code, universal_qr_url=universal_qr_url)

# Route universelle qui redirige selon le device
@app.route('/universal_qr')
def universal_qr():
    ua = request.headers.get('User-Agent', '').lower()
    if "iphone" in ua or "android" in ua:
        # Redirige vers /mobile (utilisateur)
        return redirect('/mobile')
    else:
        # Redirige vers /admin_qr (admin)
        return redirect('/admin_qr')

@app.route('/acheter')
def acheter():
    return render_template("acheter.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)