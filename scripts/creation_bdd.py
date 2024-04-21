""" 
TODO :

Lire geographie_2020.xlsx, 
Créer et remplir les tables REGIONS et DEPARTEMENTS.

Puis Lire DD-TIC-indic-reg-dep_2008_2019_2022.xls et Evolution_population_2012-2023.xlsx
Completer la base de donnée, en créant au moins 4 tables

"""

import pandas as pd
import psycopg2
import psycopg2.extras

# Fonctions
def connection(USERNAME, PASSWORD):    
    """
    Permet de se connecter au CREMI
    """

    print("Connexion à la base de données...")
    try:
        conn = psycopg2.connect(host="pgsql", dbname=USERNAME, user=USERNAME, password=PASSWORD)
    except Exception as e:
        exit("Unable to connect to the database: " + str(e))
        
    print("Connected to the database")
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return conn, cur

def execute_command(command, conn, cur, values=None):
    """
    Permet d'executer la commande sur la connection
    """
    
    try:
        if values is None:
            cur.execute(command)
        else:
            cur.execute(command, values)
        conn.commit()
        print("Commande executée avec succès")  
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        print("Error:", e)

def lire_selectif(fichier, feuille, collones, ligne_depart, nombre_de_lignes):
    return pd.read_excel("fichiers_fournis\\"+fichier,sheet_name=feuille, usecols=collones, skiprows=ligne_depart, nrows=nombre_de_lignes)

# Import des données 

departements_df = pd.read_excel("fichiers_fournis\\geographie_2020.xls", sheet_name=0) 
departements_df = departements_df.drop(departements_df.columns[2:4], axis=1)
departements_df = departements_df.drop(departements_df.columns[3:], axis=1)

regions_df = pd.read_excel("fichiers_fournis\\geographie_2020.xls", sheet_name=1)
regions_df = regions_df.drop(regions_df.columns[1:3], axis=1)
regions_df = regions_df.drop(regions_df.columns[2:], axis=1)

donnees_dep_population_df = lire_selectif("Evolution_population_2012-2023.xlsx", 0, "A:Q", 3, 101) #OK
donnees_dep_population_df = donnees_dep_population_df.drop(96) 
donnees_dep_population_df = donnees_dep_population_df.drop(donnees_dep_population_df.columns[1:5], axis=1)
donnees_dep_population_df = donnees_dep_population_df.drop(donnees_dep_population_df.columns[4:], axis=1)
donnees_dep_population_df.columns.values[0] = 'dep' 
donnees_dep_population_df.columns.values[1] = 'estimation_pop_2015'
donnees_dep_population_df.columns.values[2] = 'estimation_pop_2020'
donnees_dep_population_df.columns.values[3] = 'estimation_pop_2023'

donnees_reg_social_df = lire_selectif("DD-TIC-indic-reg-dep_2008_2019_2022.xls", 1, "A:U", 5, 17)
donnees_reg_social_df = donnees_reg_social_df.drop(donnees_reg_social_df.columns[1:17], axis=1)
donnees_reg_social_df.columns.values[0] = 'reg' 
donnees_reg_social_df.columns.values[1] = 'egloignement_sante_2021'
donnees_reg_social_df.columns.values[2] = 'egloignement_sante_2016'
donnees_reg_social_df.columns.values[3] = 'zone_inondable_2013'
donnees_reg_social_df.columns.values[4] = 'zone_inondable_2018'

donnees_reg_economie_df = lire_selectif("DD-TIC-indic-reg-dep_2008_2019_2022.xls", 2, "B:S", 5, 17)
donnees_reg_economie_df = donnees_reg_economie_df.drop(donnees_reg_economie_df.columns[1:2], axis=1)
donnees_reg_economie_df = donnees_reg_economie_df.drop(donnees_reg_economie_df.columns[3:6], axis=1)
donnees_reg_economie_df = donnees_reg_economie_df.drop(donnees_reg_economie_df.columns[5:12], axis=1)
donnees_reg_economie_df.columns.values[0] = 'reg' 
donnees_reg_economie_df.columns.values[1] = 'taux_axtivite_2019' 
donnees_reg_economie_df.columns.values[2] = 'taux_axtivite_2017' 
donnees_reg_economie_df.columns.values[3] = 'part_jeune_diplome_2014' 
donnees_reg_economie_df.columns.values[4] = 'part_jeune_diplome_2019' 
donnees_reg_economie_df.columns.values[5] = 'effort_recherche_2014' 
donnees_reg_economie_df.columns.values[6] = 'effort_recherche_2015' 

# Connection

conn, cur = connection("username", "password") # à remplacer par le mot de passe d’accès aux bases

# Création des tables
# Table regions
table_reg = """create table public.Regions(
    id_reg INT CHECK (id_reg =< 94) PRIMARY KEY NOT NULL,
    nom_reg VARCHAR NOT NULL);"""

execute_command(table_reg, conn, cur)

# Table departement
table_dep = """create table public.Departements(
    id_dep VARCHAR(3) PRIMARY KEY NOT NULL,
    id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg),
    nom_dep VARCHAR NOT NULL);"""

execute_command(table_reg, conn, cur)

# Table population
table_pop = """create table public.Population(
    id_dep VARCHAR(3) REFERENCES Departements(id_dep) NOT NULL,
    annee INT CHECK (annee =< 2024) NOT NULL,
    nombre_personnes BIGINT NOT NULL, pourcentage_inondation FLOAT CHECK (pourcentage_inondation =< 100),
    pourcentage_diplome FLOAT CHECK (pourcentage_diplome =< 100),
    taux_activité FLOAT CHECK (taux_activité =< 100));"""

execute_command(table_reg, conn, cur)

# Table Effort Recherche (ER)
table_ER = """create table public.EffortRecherche(
    id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg) NOT NULL,
    annee INT CHECK (annee =< 2024) NOT NULL,
    pourcentage_effort FLOAT CHECK (pourcentage_effort =< 100) NOT NULL,
    pourcentage_plus_7_min FLOAT CHECK (pourcentage_plus_7_min =< 100));"""

execute_command(table_reg, conn, cur)

# Table Competences numeriques (CN)
table_CN = """create table public.CompetencesNumeriques(
    id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg) NOT NULL,
    taux FLOAT CHECK (taux =< 100),
    intensite VARCHAR CONSTRAINT intensite CHECK(intensite = "fort" or intensite = "quotidienne" or intensite = "sans") NOT NULL);"""

execute_command(table_reg, conn, cur)


#Insertions des données

insert_reg = "INSERT INTO Regions (id_reg, nom_reg) VALUES (%s, %s)"
for index, row in regions_df.iterrows():
    id_reg = row['reg']
    nom_reg = row['ncc']
    cur.execute(insert_reg, (id_reg, nom_reg))

insert_dep = "INSERT INTO Departements (id_dep, id_reg, nom_dep) VALUES (%s, %s, %s)"
for index, row in departements_df.iterrows():
    id_dep = row['dep']
    id_reg = row['reg']
    nom_dep = row['ncc']
    cur.execute(insert_dep, (id_dep, id_reg, nom_dep))

insert_pop = "INSERT INTO Population (id_dep, annee, nombre_personnes, pourcentage_inondation, pourcentage_diplome, taux_activité) VALUES (%s, %s, %s,%s, %s, %s)"
# to do/ c'est un template, à adapter car il faut selectionner les lignes et donner les noms des colonnes exactes qui sont dans les fichiers
# ici les valeurs des attributs de notre table sont plustot présents dans le fichier DD-Tic... donc je ne sais pas comment inserer ces valeurs
for index, row in donnees_population_df.iterrows():
    id_dep = row['code']
    annee = row['annee']
    nombre_personnes = row['nombre_personnes']
    pourcentage_inondation = row['pourcentage_inondation']
    pourcentage_diplome = row['pourcentage_diplome']
    taux_activite = row['taux_activite']
    cur.execute(insert_pop, (id_dep, annee, nombre_personnes, pourcentage_inondation, pourcentage_diplome, taux_activite))

insert_ER = "INSERT INTO EffortRecherche (id_reg, annee, pourcentage_effort, pourcentage_plus_7_min) VALUES (%s, %s, %s)"
#to do/ c'est un template, à adapter car il faut selectionner les lignes et donner les noms des colonnes exactes qui sont dans les fichiers
for index, row in donnees_economie_df.iterrows():
    id_reg = row['id_reg'] #dans le fichier il n'y a pas de nom donné à cette colonne
    annee = row['annee']
    pourcentage_effort = row['pourcentage_effort']
    pourcentage_plus_7_min = row['pourcentage_plus_7_min']
    cur.execute(insert_ER, (id_reg, annee, pourcentage_effort, pourcentage_plus_7_min))

insert_CN = "INSERT INTO CompetencesNumeriques (id_reg, taux, intensite) VALUES (%s, %s, %s)"
#to do/c'est un template, à adapter car il faut selectionner les lignes et donner les noms des colonnes exactes qui sont dans les fichiers
for index, row in donnees_sociales_df.iterrows():
    id_reg = row['id_reg'] #dans le fichier il n'y a pas de nom donné à cette colonne
    taux = row['taux']
    intensite = row['intensite']
    cur.execute(insert_CN, (id_reg, taux, intensite))
