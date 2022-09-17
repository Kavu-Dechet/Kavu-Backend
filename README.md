# Kavu-Backend

## Details
Backend pour l'application

## Installation
* [Docker](https://docs.docker.com/engine/install/)
* [Docker compose](https://docs.docker.com/compose/install/)
* Modules python3
```bash
python3 -r requirements.txt
```
## Lancement
### Base de donnée
base de données:
```bash
docker-compose up kavu-database
# TODO: ajouter un docker-wait-for-it pour lancer backend
# docker-compose build
# docker-compose up kavu-backend
```
API (Après lancement base)
```bash
python3 dechetAPI.py
```
### API Python

Application active sur le port 5000 (http://localhost:5000/apidocs)

**NOTE** Le POST /dechet/ swagger ne fonctionne pas, utiliser curl :
```bash
#Get all dechets
curl http://localhost:5000/dechet/
# Post dechets position
curl -d "latitude=-12.9025&longitude=45.07611&categorie=VHU" -X POST "http://localhost:5000/dechet/"
# Post dechet image
curl -F "photo=@mon_image.jpg" -X POST http://localhost:5000/photo/
```


# Structure projet

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
