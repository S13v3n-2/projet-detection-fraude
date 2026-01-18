# Utiliser une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Installer les dépendances système nécessaires (si besoin pour XGBoost/Scikit-learn)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copier d'abord le fichier requirements pour profiter du cache Docker
COPY requirements.txt .

# Installer les librairies Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code source
# (On copie tout sauf ce qui est dans .dockerignore)
COPY . .

# Exposer le port sur lequel FastAPI va tourner
EXPOSE 8000

# Commande pour démarrer l'API avec Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]