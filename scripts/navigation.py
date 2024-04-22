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
            user_input = int(input(message))
            break
        except ValueError:
            print("Merci d'entrer un nombre valide")


# Voici ce que je propose. Mais pour les choix 4 et 5 j'arrive pas par ce que les années ne sont pas disponibles spécifiquement dans nos tables

# Fonction pour afficher la liste des régions disponibles
def display_regions(cur):
    cur.execute("SELECT nom_reg FROM Regions")
    regions = cur.fetchall()
    print("Régions disponibles :")
    for i, region in enumerate(regions, 1):
        print(f"{i}. {region[0]}")
    return regions


# Fonction pour afficher les départements d'une région choisie
def display_departments_of_region(cur, chosen_region):
    cur.execute("SELECT nom_dep FROM Departements WHERE id_reg = (SELECT id_reg FROM Regions WHERE nom_reg = %s)", (chosen_region,))
    departements = cur.fetchall()
    print("Départements de la région :", chosen_region)
    for i, departement in enumerate(departements, 1):
        print(f"{i}. {departement[0]}")
    return departements

# Fonction pour afficher les années disponibles pour un thème donné
def display_available_years

# Fonction pour afficher les données pour un thème et une année choisis
def display_data_for_theme_and_year

# Fonction pour imprimer la table dans un fichier CSV
def print_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)

# Fonction principale pour afficher le menu et gérer la navigation
def main():
    conn, cur = connection("username", "password")  # a remplacer par nos identifiants

    while True:
        print("\nMenu :")
        print("1. Afficher la liste des régions disponibles")
        print("2. Choisir une région et un thème")
        print("3. Afficher les départements d'une région et choisir un département")
        print("4. Choisir un thème et afficher les années disponibles")
        print("5. Choisir un thème, une année et afficher les données")
        print("6. Imprimer la table dans un fichier")
        print("7. Quitter")

        choice = input("Votre choix : ")

        if choice == "1":
            display_regions(cur)
        elif choice == "2":
            regions = display_regions(cur)
            chosen_region_index = int(input("Choisissez une région : "))
            chosen_region = regions[chosen_region_index - 1][0]
            theme_choice = int(input("Choisissez un thème :\n1. Population\n2. Social\n3. Économique\n"))
            display_available_years(cur, theme_choice, chosen_region)
        elif choice == "3":
            regions = display_regions(cur)
            chosen_region_index = int(input("Choisissez une région : "))
            chosen_region = regions[chosen_region_index - 1][0]
            display_departments_of_region(cur, chosen_region)
        elif choice == "4":
            theme_choice = int(input("Choisissez un thème :\n1. Population\n2. Social\n3. Économique\n"))
            regions = display_regions(cur)
            chosen_region_index = int(input("Choisissez une région : "))
            chosen_region = regions[chosen_region_index - 1][0]
            display_available_years(cur, theme_choice, chosen_region)
        elif choice == "5":
            theme_choice = int(input("Choisissez un thème :\n1. Population\n2. Social\n3. Économique\n"))
            regions = display_regions(cur)
            chosen_region_index = int(input("Choisissez une région : "))
            chosen_region = regions[chosen_region_index - 1][0]
            chosen_year = int(input("Choisissez une année : "))
            display_data_for_theme_and_year(cur, theme_choice, chosen_region, chosen_year)
        elif choice == "6":
            filename = input("Entrez le nom du fichier CSV à créer (avec extension .csv) : ")
            data = input("Entrez les données à écrire dans le fichier (sous forme de liste de listes) : ")
            print_to_csv(data, filename)
            print("La table a été imprimée dans le fichier", filename)
        elif choice == "7":
            break
        else:
            print("Veuillez choisir une option valide.")

    conn.close()

if __name__ == "__main__":
    main()














