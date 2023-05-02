# Créé par Lionel, le 05/01/2023 en Python 3.7
fichier_coord = "./libs/localisation/communes/communes-20220101-OSM-Mayotte.geojson"
import json


def trouver_commune(latitude, longitude):
    with open(fichier_coord) as contours:
        communes = json.load(contours)
    point_temp = [float(longitude), float(latitude)]
    for feature in communes['features']:

        coordinates = feature['geometry']['coordinates']
        nom_commune = feature['properties']['nom']
        for coordinate in coordinates:
            for polygone in coordinate:
                if point_dans_polygone(polygone, point_temp):
                    print("le point est dans la commune de", nom_commune, sep=" ")
                    return nom_commune

    return "none"


def point_dans_polygone(polygone, point):
    # Un point est dans ou sur un polygone si une demi-droite ayant pour origine ce point coupe les arrêtes du polygone un nombre impair de fois.
    # Un arrête est définie par le segment ayant pour extrémités deux sommets consécutifs du polygone
    impair = False
    compteur = 0
    i = 0
    j = len(polygone) - 1

    while i < len(polygone):

        # Si le point est sur un sommet :
        if point == polygone[i] or point == polygone[j]:
            print("le point est sur un sommet")
            return True

        # Si le point est sur une arrête horizontale :
        if (
                min(polygone[i][0], polygone[j][0]) < point[0] < max(polygone[i][0], polygone[j][0])
                and polygone[i][1] == polygone[j][1] == point[1]
        ):
            print("le point est sur une arrête horizontale")
            return True

        # Si le point est sur une arrête verticale :
        if (
                min(polygone[i][1], polygone[j][1]) < point[1] < max(polygone[i][1], polygone[j][1])
                and polygone[i][0] == polygone[j][0] == point[0]
        ):
            print("le point est sur une arrête verticale")
            return True

        # Si le point est sur une arrête oblique :
        if (
                min(polygone[i][0], polygone[j][0]) < point[0] < max(polygone[i][0], polygone[j][0])
                and polygone[i][1] != polygone[j][1] and polygone[i][1] != point[1] and polygone[j][1] != point[1]
                and (point[1] - polygone[i][1]) / (point[0] - polygone[i][0]) == (polygone[j][1] - polygone[i][1]) / (
                polygone[j][0] - polygone[i][0])
        ):
            print("le point est sur une arrête oblique")
            return True

        # La demi-droite horizontale orientée vers +inf passant par le point coupe une arrête oblique ou verticale en passant strictement entre ses extrémités
        # L'ordonnée du point est strictement comprise entre celles des extrémités du segment
        # L'abscisse du point se situe à gauche de celle de son projeté horizontal sur le segment
        # La parité est inversée si ces conditions sont réunies
        if (
                min(polygone[i][1], polygone[j][1]) < point[1] < max(polygone[i][1], polygone[j][1])
                and point[0] < (polygone[j][0] - polygone[i][0]) / (polygone[j][1] - polygone[i][1]) * (
                point[1] - polygone[i][1]) + polygone[i][0]
        ):
            print("la demi-droite passant par le point croise une arrête oblique ou verticale")
            impair = not impair

        # La demi-droite horizontale orientée vers +inf passant par le point coupe une arrête oblique ou verticale en passant par une de ses extrémités
        # L'ordonnée du point est égale à l'ordonnée d'une seule des deux extrémités du segment (sinon le segment est horizontal et il ne "compte pas".
        # L'abscisse du point se situe à gauche de celle de son projeté horizontal sur le segment
        # On met en place un compteur la 1ère fois que cette configuration est rencontrée : si le point est au-dessus du segment alors +1, sinon -1.
        # Ainsi, la fois suivante, si le point change de position alors le compteur s'annule et la bordure du polygone est considérée comme traversée, sinon le point reste du même côté (la droite horizontale est tangente à un sommet) et la bordure est considérée comme n'étant pas traversée, le compteur est remis à 0.
        # La parité est inversée à chaque annulation non forcée du compteur
        if (
                min(polygone[i][1], polygone[j][1]) == point[1] < max(polygone[i][1], polygone[j][1]) or min(
            polygone[i][1], polygone[j][1]) < point[1] == max(polygone[i][1], polygone[j][1])
                and (polygone[j][0] - polygone[i][0]) / (polygone[j][1] - polygone[i][1]) * (
                point[1] - polygone[i][1]) + polygone[i][0] > point[0]
        ):
            if compteur != 0:
                if point[1] == min(polygone[i][1], polygone[j][1]):
                    compteur = compteur - 1
                if point[1] == max(polygone[i][1], polygone[j][1]):
                    compteur = compteur + 1
                if compteur == 0:
                    impair = not impair
                    print("la demi-droite horizontale passant par le point coupe une bordure au niveau d'un sommet")
                else:
                    compteur = 0
            else:
                if point[1] == min(polygone[i][1], polygone[j][1]):
                    compteur = compteur - 1
                if point[1] == max(polygone[i][1], polygone[j][1]):
                    compteur = compteur + 1
        j = i
        i = i + 1

    return impair
