# Utilise une image Python officielle
FROM python:3.13-slim

# Définit le répertoire de travail
WORKDIR /app

# Copie les fichiers du projet
COPY . /app

# Met à jour les paquets système et installe les dépendances
RUN apt-get update && apt-get upgrade -y \
    && pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Expose le port Flask
EXPOSE 10000

# Commande de lancement
CMD ["python", "app.py"]
