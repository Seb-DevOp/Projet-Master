FROM python:3.11-slim

# Éviter les interactions lors de apt install
ENV DEBIAN_FRONTEND=noninteractive

# Définir le répertoire de travail
WORKDIR /app

# Copier uniquement les requirements au début pour tirer parti du cache Docker
COPY requirements.txt .

# Installer les dépendances système nécessaires pour compiler certains packages Python
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libssl-dev \
        libffi-dev \
        python3-dev \
        && rm -rf /var/lib/apt/lists/*

# Mettre pip à jour
RUN pip install --upgrade pip

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du projet
COPY . .

# Commande par défaut pour lancer le script
CMD ["python", "SimulateData.py"]
