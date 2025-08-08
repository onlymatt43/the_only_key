# Révision du code Fiche technique administrateur – The Only Key

## 1. Prérequis
- Accès au serveur (hébergement Python/Flask, accès SSH recommandé)
- Navigateur web moderne (mobile et desktop)
- QR code admin (QR :roi) généré à l’installation
- Mot de passe admin (défini dans le code, à changer avant production)

## 2. Démarrage initial
1. **Installation**
   - Déployer le dossier du projet sur le serveur.
   - Installer les dépendances Python (`pip install -r requirements.txt`).
   - Lancer l’application (`python app.py`).
2. **Sécurisation**
   - Activer HTTPS (recommandé pour la production).
   - Changer le mot de passe admin dans `app.py` (`ADMIN_PASSWORD`).
   - Protéger l’accès au serveur et aux fichiers sensibles (`token_store.json`, `roi_token.json`, `access.log`).

## 3. Gestion des accès
- **QR admin (QR :roi)** :
  - Le premier QR :roi scanné sur mobile devient le super-admin, figé à vie.
  - Ce QR permet d’accéder à toutes les pages protégées, sans limite.
  - Ne jamais partager ce QR, il n’est ni réinitialisable ni transférable.
- **QR utilisateurs** :
  - Générer des QR personnalisés via `/admin_qr` (accès protégé par mot de passe).
  - Associer chaque QR à une durée et une page à débloquer.

## 4. Interface d’administration
- **/admin_qr** : Générateur de QR codes (accès protégé).
- **/admin_tokens** : Liste, audit et suppression des tokens actifs/expirés (accès protégé).
- **Mot de passe admin** : Requis à chaque nouvelle session ou après expiration du cookie.

## 5. Sécurité & maintenance
- **Logs** :
  - Toutes les tentatives d’accès (succès, échecs, blocages) sont enregistrées dans `access.log`.
  - Surveiller ce fichier pour détecter des abus ou tentatives de brute-force.
- **Anti-bruteforce** :
  - Limite de 10 tentatives par IP sur 5 minutes pour l’accès utilisateur.
- **Sauvegardes** :
  - Sauvegarder régulièrement `token_store.json` et `roi_token.json`.
- **Mises à jour** :
  - Mettre à jour le code et les dépendances en cas de faille ou d’évolution.

## 6. Bonnes pratiques
- Ne jamais diffuser le QR :roi.
- Changer le mot de passe admin par défaut.
- Utiliser HTTPS.
- Restreindre l’accès SSH/FTP au serveur.
- Surveiller les logs et supprimer les tokens expirés ou suspects.

---

**En cas de perte du QR :roi, il n’y a pas de récupération possible.**
Sauvegarder ce QR dans un coffre-fort numérique dès la première utilisation.
