# Guide installation serveur – The Only Key

## 1. Prérequis
- Serveur Linux (Ubuntu recommandé) ou macOS
- Python 3.8+
- Accès SSH/FTP pour déployer les fichiers
- (Optionnel) Nom de domaine et certificat SSL (HTTPS)

## 2. Installation
1. **Transfert des fichiers**
   - Copier tout le dossier du projet sur le serveur (via SCP, SFTP, etc.).
2. **Installation des dépendances**
   - Se placer dans le dossier du projet
   - Installer les dépendances :
     ```
     pip install -r requirements.txt
     ```
3. **Configuration**
   - Modifier le mot de passe admin dans `app.py` (`ADMIN_PASSWORD`)
   - (Optionnel) Configurer un domaine et un certificat SSL
4. **Lancement**
   - Démarrer l’application :
     ```
     python app.py
     ```
   - Accéder à l’URL du serveur (ex : http://localhost:5050)

## 3. Sécurité
- Utiliser HTTPS en production
- Restreindre l’accès SSH/FTP
- Protéger les fichiers sensibles (`token_store.json`, `roi_token.json`, `access.log`)
- Sauvegarder régulièrement les fichiers de données

## 4. Maintenance
- Mettre à jour le code et les dépendances si besoin
- Surveiller les logs d’accès (`access.log`)
- Nettoyer les tokens expirés via l’interface admin

---

**Le QR roi n’est généré qu’une seule fois et ne peut jamais être réinitialisé.**
Sauvegardez-le dès la première utilisation.
