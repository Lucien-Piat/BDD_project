""" 
TODO :

Lire geographie_2020.xls, 
Créer et remplir les tables REGIONS et DEPARTEMENTS.

Puis Lire DD-TIC-indic-reg-dep_2008_2019_2022.xls et Evolution_population_2012-2023.xls
Completer la base de donnée, en créant au moins 4 tables

"""

import pandas as pd
import psycopg2
import psycopg2.extras

# Faudra tenir compte qu'il ya plusieurs feuilles par fichier, il faut surement créer une dataframe pour chaque feuille (table)
# Par exemple geographie_2020.xls contient les feuilles regions et departement pour nos tables regions et departements
# On va créer une dataframe pour lire les feuilles nécéssaires 
# Lire les données géographiques
geographie_df = pd.read_excel("geographie_2020.xls")

# Lire les données sociales et économiques
donnees_sociales_df = pd.read_excel("DD-TIC-indic-reg-dep_2008_2019_2022.xls")
donnees_population_df = pd.read_excel("Evolution_population_2012-2023.xls")


# Try to connect to an existing database
print("Connexion à la base de données...")
USERNAME="username"
PASSWORD="password" # à remplacer par le mot de passe d’accès aux bases
try:
    conn = psycopg2.connect(host='pgsql', dbname=USERNAME,user=USERNAME, password=PASSWORD)
except Exception as e :
    exit("Connexion impossible à la base de données: " + str(e))
    
print("Connecté à la base de données")
#préparation de l’exécution des requêtes (à ne faire qu’une fois)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)



# Création des tables
# Table regions
table_reg = "create table public.Regions(id_reg INT CHECK (id_reg =< 94) PRIMARY KEY NOT NULL, nom_reg VARCHAR NOT NULL);"
cur.execute(table_reg)

# Table departement
table_dep = "create table public.Departements(id_dep VARCHAR(3) PRIMARY KEY NOT NULL, id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg), nom_dep VARCHAR NOT NULL);"
cur.execute(table_dep)

# Table population
table_pop = "create table public.Population(id_dep VARCHAR(3) REFERENCES Departements(id_dep) NOT NULL, annee INT CHECK (annee =< 2024) NOT NULL, nombre_personnes BIGINT NOT NULL, pourcentage_inondation FLOAT CHECK (pourcentage_inondation =< 100), pourcentage_diplome FLOAT CHECK (pourcentage_diplome =< 100), taux_activité FLOAT CHECK (taux_activité =< 100));"
cur.execute(table_pop)

# Table Effort Recherche (ER)
table_ER = "create table public.EffortRecherche(id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg) NOT NULL, annee INT CHECK (annee =< 2024) NOT NULL, pourcentage_effort FLOAT CHECK (pourcentage_effort =< 100) NOT NULL, pourcentage_plus_7_min FLOAT CHECK (pourcentage_plus_7_min =< 100))"
cur.execute(table_ER)

# Table Competences numeriques (CN)
table_CN = "create table public.CompetencesNumeriques(id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg) NOT NULL, taux FLOAT CHECK (taux =< 100), intensite VARCHAR CONSTRAINT intensite CHECK(intensite = "fort" or intensite = "quotidienne" or intensite = "sans") NOT NULL)"
cur.execute(table_CN)

#Insertions des données

insert_reg = "INSERT INTO Regions (id_reg, nom_reg) VALUES (%s, %s)"
#to do

insert_dep = "INSERT INTO Departements (id_dep, id_reg, nom_dep) VALUES (%s, %s, %s)"
#to do

insert_pop = "INSERT INTO Population (id_dep, annee, nombre_personnes, pourcentage_inondation, pourcentage_diplome, taux_activité) VALUES (%s, %s, %s,%s, %s, %s)"
#to do

insert_ER = "INSERT INTO EffortRecherche (id_reg, annee, pourcentage_effort, pourcentage_plus_7_min) VALUES (%s, %s, %s)"
#to do

insert_CN = "INSERT INTO CompetencesNumeriques (id_reg, taux, intensite) VALUES (%s, %s, %s)"
#to do
