# Utiliser une image Python légère comme base
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier tout le contenu du projet dans le conteneur
COPY . /app

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Exposer les ports nécessaires (API Flask et Streamlit)
EXPOSE 5001 8501

# Installer supervisord pour gérer plusieurs processus
RUN pip install supervisor

# Copier le fichier de configuration supervisord
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Commande d'exécution : lancer supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
