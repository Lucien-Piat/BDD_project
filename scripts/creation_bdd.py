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
    estimation_pop_2015 BIGINT NOT NULL, estimation_pop_2020 BIGINT NOT NULL, estimation_pop_2023 BIGINT NOT NULL,
    zone_inondable_2013 FLOAT CHECK (zone_inondable_2013 =< 100), 
    zone_inondable_2018 FLOAT CHECK (zone_inondable_2018 =< 100),
    part_jeune_diplome_2014 FLOAT CHECK (part_jeune_diplome_2014 =< 100),
    part_jeune_diplome_2019 FLOAT CHECK (part_jeune_diplome_2019 =< 100),
    taux_activite_2019 FLOAT CHECK (taux_activite_2019 =< 100)
    taux_activite_2017 FLOAT CHECK (taux_activite_2017 =< 100));"""

execute_command(table_pop, conn, cur)

# Table Effort Recherche (ER)
table_ER = """create table public.EffortRecherche(
    id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg) NOT NULL,
    effort_recherche_2014 FLOAT CHECK (effort_recherche_2014 =< 100) NOT NULL,
    effort_recherche_2015 FLOAT CHECK (effort_recherche_2015 =< 100) NOT NULL,
    egloignement_sante_2021 FLOAT CHECK (egloignement_sante_2021 =< 100),
    egloignement_sante_2016 FLOAT CHECK (egloignement_sante_2016 =< 100));"""

execute_command(table_ER, conn, cur)

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

# J'essayes de fusionner les fichiers
# Pour la table Populaton je constate que nous avons besoin des fichiers: donnees_reg_economie_df, donnees_reg_social_df et donnees_dep_population_df
# Pour fusionner les trois nous allons d'abord faire une premiere fusion, et une deuxieme fusion apartir de la premiere fusion
# Fusionner les deux fichiers sur leurs colonnes communes
merged_pop_df = pd.merge(donnees_reg_economie_df, donnees_reg_social_df, on='reg')

# Concaténer le résultat de la fusion avec les données du troisième fichier qui n'a pas de colonne en commun
final_pop_def = pd.concat([merged_pop_df, donnees_dep_population_df], axis=0)


insert_pop = "INSERT INTO Population (id_dep, estimation_pop_2015, estimation_pop_2020, estimation_pop_2023, zone_inondable_2013, zone_inondable_2018, part_jeune_diplome_2014, part_jeune_diplome_2019, taux_activite_2019, taux_activite_2017) VALUES (%s, %s,%s, %s, %s, %s, %s,%s, %s, %s)"
# to do/ c'est un template, à adapter car il faut selectionner les lignes et donner les noms des colonnes exactes qui sont dans les fichiers
# ici les valeurs des attributs de notre table sont plustot présents dans le fichier DD-Tic... donc je ne sais pas comment inserer ces valeurs
for index, row in final_pop_def.iterrows():
    id_dep = row['code']
    #annee = row['annee'] # ça il faut enlever? pareil pour toutes les tables ou ya année
    estimation_pop_2015 = row['estimation_pop_2015']
    estimation_pop_2020 = row['estimation_pop_2020']
    estimation_pop_2023 = row['estimation_pop_2023']
    zone_inondable_2013 = row['zone_inondable_2013']
    zone_inondable_2018 = row['zone_inondable_2018']
    part_jeune_diplome_2014 = row['part_jeune_diplome_2014']
    part_jeune_diplome_2019 = row['part_jeune_diplome_2019']
    taux_activite_2019 = row['taux_activite_2019']
    taux_activite_2017 = row['taux_activite_2017']
    cur.execute(insert_pop, (id_dep, estimation_pop_2015, estimation_pop_2020, estimation_pop_2023, zone_inondable_2013, zone_inondable_2018, part_jeune_diplome_2014, part_jeune_diplome_2019, taux_activite_2019, taux_activite_2017))

# J'essayes de fusionner les fichiers
# Pour la table EffortRecherche je constate que nous avons besoin des fichiers: donnees_reg_economie_df et donnees_reg_social_df
# Pour fusionner les trois nous allons d'abord faire une premiere fusion, et une deuxieme fusion apartir de la premiere fusion
# Fusionner les deux fichiers sur leurs colonnes communes
# merged_ER_df = pd.merge(donnees_reg_economie_df, donnees_reg_social_df, on='reg')

merged_ER_df = pd.merge(donnees_reg_economie_df, donnees_reg_social_df, on='reg')
insert_ER = "INSERT INTO EffortRecherche (id_reg, effort_recherche_2014, effort_recherche_2015, egloignement_sante_2021, egloignement_sante_2016) VALUES (%s, %s, %s, %s, %s)"

#to do/ c'est un template, à adapter car il faut selectionner les lignes et donner les noms des colonnes exactes qui sont dans les fichiers
for index, row in merged_ER_df.iterrows():
    id_reg = row['reg']
    effort_recherche_2014 = row['effort_recherche_2014']
    effort_recherche_2015 = row['effort_recherche_2015']
    egloignement_sante_2021 = row['egloignement_sante_2021']
    egloignement_sante_2016 = row['egloignement_sante_2016']
    cur.execute(insert_ER, (id_reg, effort_recherche_2014, effort_recherche_2015, egloignement_sante_2021, egloignement_sante_2016))

# Du coup cette table et cette insertion ne sont pas nécéessaire, si? par ce que dans les fichiers que t'a créer je ne trouve pas de correspondance
# Sauf si je me trompe
insert_CN = "INSERT INTO CompetencesNumeriques (id_reg, taux, intensite) VALUES (%s, %s, %s)"
#to do/c'est un template, à adapter car il faut selectionner les lignes et donner les noms des colonnes exactes qui sont dans les fichiers
for index, row in donnees_sociales_df.iterrows():
    id_reg = row['id_reg'] #dans le fichier il n'y a pas de nom donné à cette colonne
    taux = row['taux']
    intensite = row['intensite']
    cur.execute(insert_CN, (id_reg, taux, intensite))
