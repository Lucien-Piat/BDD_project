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



# Lire les données géographiques
departements_df = pd.read_excel("geographie_2020.xls", sheet_name=1)
regions_df = pd.read_excel("geographie_2020.xls", sheet_name=2) # On précise la feuille a lire

# Lire les données sociales et économiques
donnees_population_df = pd.read_excel("Evolution_population_2012-2023.xls",sheet_name=1)
donnees_sociales_df = pd.read_excel("DD-TIC-indic-reg-dep_2008_2019_2022.xls", sheet_name=2)
donnees_economie_df = pd.read_excel("DD-TIC-indic-reg-dep_2008_2019_2022.xls", sheet_name=3)

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

# C'est pas un truc comme ca ? 
"intensite TEXT NOT NULL CHECK (rang IN ('fort', 'quotidienne', 'sans')"

execute_command(table_reg, conn, cur)

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
