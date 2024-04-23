import pandas as pd
import psycopg2
import psycopg2.extras

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
        print("Error:", e)

def lire_selectif(fichier, feuille, collones, ligne_depart, nombre_de_lignes):
    return pd.read_excel("fichiers_fournis\\"+fichier,sheet_name=feuille, 
                         usecols=collones, 
                         skiprows=ligne_depart, 
                         nrows=nombre_de_lignes)

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

""" Pour la connection en local """ 
conn = psycopg2.connect(
    host="localhost",
    dbname="public",
    user="postgres",
    password="superlucienpiat"
)
cur = conn.cursor()

""" Pour la connection au cremi """
# conn, cur = connection("username", "password")

####################################
###  Creation de la table Region ### 

table_reg = """create table public.Regions (
    id_reg INT CHECK (id_reg <= 94) PRIMARY KEY NOT NULL,
    nom_reg VARCHAR NOT NULL);"""

execute_command(table_reg, conn, cur)

# Extraction des données
regions_df = pd.read_excel("fichiers_fournis\\geographie_2020.xls", sheet_name=1)
regions_df = regions_df.drop(regions_df.columns[1:3], axis=1)
regions_df = regions_df.drop(regions_df.columns[2:], axis=1)

# Population de la table
insert_reg = "INSERT INTO Regions (id_reg, nom_reg) VALUES (%s, %s)"
for i in range(regions_df.shape[0]):
    lst = list(regions_df.iloc[i])
    lst[0] = int(lst[0])
    values_tuple = tuple(lst)
    execute_command(insert_reg, conn, cur, values=lst)

########################################
### Creation de la table Departement ### 

table_dep = """create table public.Departements (
    id_dep VARCHAR(3) PRIMARY KEY NOT NULL,
    id_reg INT CHECK (id_reg <= 94) REFERENCES public.Regions(id_reg),
    estimation_pop_2015 BIGINT, estimation_pop_2020 BIGINT , estimation_pop_2023 BIGINT,
    nom_dep VARCHAR NOT NULL);"""

execute_command(table_dep, conn, cur)

# Extraction des données de départements
departements_df = pd.read_excel("fichiers_fournis\\geographie_2020.xls", sheet_name=0) 
departements_df = departements_df.drop(departements_df.columns[2:4], axis=1)
departements_df = departements_df.drop(departements_df.columns[3:], axis=1)
departements_df.columns.values[0] = 'dep'

# Extraction des données de population
donnees_dep_population_df = lire_selectif("Evolution_population_2012-2023.xlsx", 0, "A:Q", 3, 101)
donnees_dep_population_df = donnees_dep_population_df.drop(96) # Retrait des données parasites 
donnees_dep_population_df = donnees_dep_population_df.drop(donnees_dep_population_df.columns[1:5], axis=1)
donnees_dep_population_df = donnees_dep_population_df.drop(donnees_dep_population_df.columns[4:], axis=1)
donnees_dep_population_df.columns = ['dep', 'estimation_pop_2015', 'estimation_pop_2020', 'estimation_pop_2023']

# On doit ajouter une ligne pour mayotte
new_row = pd.DataFrame({'dep': ['976'], 'estimation_pop_2015': [None], 'estimation_pop_2020': [None], 'estimation_pop_2023': [None]})
donnees_dep_population_df = pd.concat([donnees_dep_population_df, new_row], ignore_index=True)

# On doit transformer les "1" en "01" pour le merge 
departements_df['dep'] = departements_df['dep'].astype(str)
for i in range(9):
    departements_df.loc[i, "dep"] = "0"+departements_df.loc[i, "dep"]

# On merge sur le nom du département
departements_df = pd.merge(departements_df, donnees_dep_population_df, on='dep')

insert_dep = """INSERT INTO Departements (
    id_dep, 
    id_reg, nom_dep, 
    estimation_pop_2015, 
    estimation_pop_2020, 
    estimation_pop_2023) 
    VALUES (%s, %s, %s, %s, %s, %s)"""

for i in range(departements_df.shape[0]):
    lst = list(departements_df.iloc[i])
    lst[1] = int(lst[1])
    try : 
        lst[3] = int(lst[3])
        lst[4] = int(lst[4])
        lst[5] = int(lst[5])
    except TypeError as e:
        # Pour mayotte on ajoute des valeures nulles
        print("Ajout de cases vides")
    values_tuple = tuple(lst)
    execute_command(insert_dep, conn, cur, values=lst)



####################################
###  Creation de la table Social ### 

table_pop = """create table public.Social(
    id_reg INT CHECK (id_reg <= 94) REFERENCES public.Regions(id_reg) NOT NULL, 
    zone_inondable_2013 FLOAT CHECK (zone_inondable_2013 <= 100), 
    zone_inondable_2018 FLOAT CHECK (zone_inondable_2018 <= 100),
    egloignement_sante_2021 FLOAT CHECK (egloignement_sante_2021 <= 100),
    egloignement_sante_2016 FLOAT CHECK (egloignement_sante_2016 <= 100));"""

execute_command(table_pop, conn, cur)

# Extraction des données
donnees_reg_social_df = lire_selectif("DD-TIC-indic-reg-dep_2008_2019_2022.xls", 1, "A:U", 5, 17)
donnees_reg_social_df = donnees_reg_social_df.drop(donnees_reg_social_df.columns[1:17], axis=1)
donnees_reg_social_df.columns = ['reg', 
                                   'egloignement_sante_2021', 
                                   'egloignement_sante_2016', 
                                   'zone_inondable_2013', 
                                   'zone_inondable_2018']

# On remplace les Nd par des None 
donnees_reg_social_df.replace('nd', None, inplace=True)

# Population de la table
insert_social = """INSERT INTO social (id_reg, 
    egloignement_sante_2021, 
    egloignement_sante_2016, zone_inondable_2013, 
    zone_inondable_2018) 
    VALUES (%s, %s, %s, %s, %s)"""

for i in range(donnees_reg_social_df.shape[0]):
    lst = list(donnees_reg_social_df.iloc[i])
    lst[0] = int(lst[0])
    values_tuple = tuple(lst)
    execute_command(insert_social, conn, cur, values=lst)


######################################
###  Creation de la table Economie ### 

table_eco = """create table public.Economie(
    id_reg INT CHECK (id_reg <= 94) REFERENCES public.Regions(id_reg) NOT NULL,
    taux_activite_2019 FLOAT CHECK (taux_activite_2019 <= 100),
    taux_activite_2017 FLOAT CHECK (taux_activite_2017 <= 100),
    part_jeune_diplome_2014 FLOAT CHECK (part_jeune_diplome_2014 <= 100),
    part_jeune_diplome_2009 FLOAT CHECK (part_jeune_diplome_2009 <= 100),
    effort_recherche_2014 FLOAT CHECK (effort_recherche_2014 <= 100) NOT NULL,
    effort_recherche_2010 FLOAT CHECK (effort_recherche_2010 <= 100) NOT NULL
    );"""

execute_command(table_eco, conn, cur)

# Extraction des données
donnees_reg_economie_df = lire_selectif("DD-TIC-indic-reg-dep_2008_2019_2022.xls", 2, "B:S", 5, 17)
donnees_reg_economie_df = donnees_reg_economie_df.drop(donnees_reg_economie_df.columns[1:2], axis=1)
donnees_reg_economie_df = donnees_reg_economie_df.drop(donnees_reg_economie_df.columns[3:6], axis=1)
donnees_reg_economie_df = donnees_reg_economie_df.drop(donnees_reg_economie_df.columns[5:12], axis=1)
donnees_reg_economie_df.columns = ['reg', 
                                   'taux_activite_2019', 
                                   'taux_activite_2017', 
                                   'part_jeune_diplome_2014', 
                                   'part_jeune_diplome_2009' , 
                                   'effort_recherche_2014' , 
                                   'effort_recherche_2010']

# Population de la table

insert_eco = """INSERT INTO Economie (
    id_reg, taux_activite_2019,
    taux_activite_2017, part_jeune_diplome_2014,
    part_jeune_diplome_2009,
    effort_recherche_2014,
    effort_recherche_2010) 
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

for i in range(donnees_reg_economie_df.shape[0]):
    lst = list(donnees_reg_economie_df.iloc[i])
    lst[0] = int(lst[0])
    values_tuple = tuple(lst)
    execute_command(insert_eco, conn, cur, values=lst)

######################################
###  Creation de la table CompNum ### 

table_cn = """create table public.CompNum(
    id_reg INT CHECK (id_reg <= 94) REFERENCES public.Regions(id_reg) NOT NULL,
    cn_forte FLOAT CHECK (cn_forte <= 100),
    cn_quotidienne FLOAT CHECK (cn_quotidienne <= 100),
    cn_sans FLOAT CHECK (cn_sans <= 100)
    );"""

execute_command(table_cn, conn, cur)

# Extraction des données
donnees_reg_cn_df = lire_selectif("DD-TIC-indic-reg-dep_2008_2019_2022.xls", 2, "B:V", 5, 17)
donnees_reg_cn_df = donnees_reg_cn_df.drop(donnees_reg_cn_df.columns[1:18], axis=1)
donnees_reg_cn_df.columns = ['reg', 'cn_forte', 'cn_quotidienne', 'cn_sans']
donnees_reg_cn_df.replace('nd', None, inplace=True)

# Population de la table
insert_cn = """INSERT INTO CompNum (
    id_reg, 
    cn_forte, 
    cn_quotidienne, 
    cn_sans) 
    VALUES (%s, %s, %s, %s)"""

for i in range(donnees_reg_cn_df.shape[0]):
    lst = list(donnees_reg_cn_df.iloc[i])
    lst[0] = int(lst[0])
    values_tuple = tuple(lst)
    execute_command(insert_cn, conn, cur, values=lst)