"""
TODO : 

1. Afficher la liste des régions disponibles et demander à l'utilisateur de choisir une région puis : 

Soit : 
2. Demander à l'utilisateur de choisir un thème : population, social, économique puis aller en 6

3. Afficher les départements de la région choisie et demander à l'utilisateur de choisir un département de la région
4. Demander à l 'utilisateur de choisir un thème : population, social, économique et afficher les années disponibles pour le theme choisi
5. Demander à l 'utilisateur de choisir un une année disponible et afficher les donnés pour le thème et l'année choisi (pour la région ou le département)

6. Proposer l'impression de la table dans un fichier ou de retourner au départ du menu

"""

import pandas as pd
import psycopg2 
import psycopg2.extras
from creation_bdd import connection, execute_command

def print_and_wait(message, list_des_choix):
    while True:
        try:
            input = int(input(message))
            break
        except ValueError:
            print("Merci d'entrer un nombre valide")

