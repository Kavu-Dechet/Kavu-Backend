# Kavu-Backend

## Fonctionnement
L'application Kavu permet de géolocaliser des déchets : 

<img src=".README/kavu-usage.png">

## Details de l'API
L'API est en python, elle fait l'intermédiaire entre les requêtes et la base de données.

## Installation (~5 min)

### Installation de la base de données
La base de données de test que nous utilisons est sous docker.
Pour installer docker et docker-compose :
* [Docker](https://docs.docker.com/engine/install/)
* [Docker compose](https://docs.docker.com/compose/install/)
Pour vérifier l'installation tester les commandes ci-dessous : 
```bash
docker --version
docker-compose --version
docker run hello-world
```
### Installation des modules python (~2 mins)
L'application utilise le framework flask, ainsi que plusieurs modules. Pour effectuer une installation complète :
```bash
pip install -r python-backend/requirements.txt -v
```

## Lancement
### Base de données
Une fois docker et docker-compose installés, vous pouvez lancer la base de données :
```bash
cd python-backend
docker-compose up kavu-backend &
```
Une base est lancée et disponible au port 5432 (les informations de la base se trouvent dans le fichier docker-compose.yml).

### API Python
une fois la base prête, vous pouvez lancer l'API python : 
```bash
python3 dechetAPI.py
```
Application active sur le port 5000 (http://localhost:5000/apidocs)

**NOTE** Le POST /dechet/ swagger ne fonctionne pas, utiliser curl :
```bash
# Récupération de tous les déchets
curl http://localhost:5000/dechet/
# Post d'un dechets
curl -d "latitude=-12.9025&longitude=45.07611&categories=d3e,vhu" -X POST "http://localhost:5000/dechet/"
# Post dechet image
curl -F "photo=@mon_image.jpg" -X POST http://localhost:5000/photo/
```

## Structure projet

## Base de données
<img src=".README/kavu_db_schema.png">

## Python
Le point d'entrée est dechetAPI. Il s'agit d'une API Python Flask au format REST. La documentation des méthodes est automatiquement chargée par le module Swagger (endpoint /apidocs )

## persistence
Le dossier dossier contient toute les opérations sur la base de données :
* config_persistence permet d'initialiser la base si cette dernière est vierge
* crud_persistence gère toutes les sauvegardes de déchets (hors image)
* images_persistences sauvegardes les images de déchets

## Docker
* Le fichier Dockerfile permet de définir comment construire une image Docker/Kavu-Back
* Le fichier docker-compose.yml est regroupe toutes les composants du back (base + API python)


# Ressources
[posgres A trier](https://www.postgresqltutorial.com/postgresql-python/connect/)

# Changement Version
* Pusher le répo
* Merge request sur master/main

* Tagger le repo git tag V.x.x
* Aller sur Pikachu -> Répertoire python-backend
* Attention ne pas faire d'actions docker irréversibles (up/build/down risqués... passer par le script update-backend.sh)
```sh 
# Vérifier que c'est la branche master/main
git branch

# Faire git status   -> Trois fichiers doivents être en cours de moidifications (vert ou rouge) : docker-compose.yml,  persistence/docker_database.ini et update-backend.sh
git status

# Faire un git stash pour oublier temporairement les modifications
git stash

# Faire un git pull
git pull

# Faire git stash pop pour resortir les configs
git stash pop

# Ne pas lancer de commandes docker ! Utiliser le script conçus pour ça :
./update-backend.sh

```

Vérifier l'endpoint : http://51.68.90.188:5500/apidocs/