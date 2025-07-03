# Visualiseur de Logs en Temps Réel

Ce projet fournit une interface web pour visualiser et rechercher des fichiers de logs en temps réel grâce à FastAPI et Docker.

## Prérequis

- [Docker](https://www.docker.com/) installé
- (Optionnel) [Docker Compose](https://docs.docker.com/compose/)

## Utilisation rapide avec Docker

1. **Cloner le dépôt :**
   ```sh
   git clone <votre-repo>
   cd LogViewer
   ```

2. **Construire et lancer le conteneur avec Docker Compose :**
   ```sh
   docker-compose up --build
   ```

   L'application sera accessible sur [http://localhost:7777](http://localhost:7777).

3. **Ajouter vos fichiers de logs :**
   Placez vos fichiers de logs dans le dossier `app/logs/` pour qu'ils soient accessibles via l'interface.

## Variables d'environnement

- `LOGS_EXTENSIONS` : Extensions de fichiers à afficher (par défaut `.log,.txt`)
- `LOGS_DIRECTORY` : Dossier des logs dans le conteneur (par défaut `/logs`)

Vous pouvez les personnaliser dans le fichier [`docker-compose.yaml`](docker-compose.yaml).

## Accès à l'interface

- Ouvrez votre navigateur à l'adresse : [http://localhost:7777](http://localhost:7777)
- Utilisez les outils de recherche, filtrage, navigation et téléchargement intégrés.

## Commandes Docker manuelles

Pour construire et lancer sans Docker Compose :

```sh
docker build -t logviewer ./app
docker run -d -p 7777:80 -v $(pwd)/app/logs:/app/logs --name logviewer logviewer
```

## Structure du projet

- [`app/app.py`](app/app.py) : Application FastAPI principale
- [`app/templates/index.html`](app/templates/index.html) : Interface utilisateur
- [`app/logs/`](app/logs/) : Dossier pour vos fichiers de logs

## Licence

MIT