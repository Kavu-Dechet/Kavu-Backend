# Kavu-Backend

## Details
Backend pour l'application

## Installation
python3
```bash
python3 -r requirements.txt
```

## Lancement
### Base de donnée
En mode dev :
```bash
# Si ca ne marche pas faire docker-compose up
docker-compose start  kavu-database
```

### API Python
(Après lancement base)
```bash
python3 dechetAPI.py
```
Application active sur le port 5000 (http://localhost:5000)
