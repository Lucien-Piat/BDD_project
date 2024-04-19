""" 
TODO :

Lire geographie_2020.xlsx, 
Créer et remplir les tables REGIONS et DEPARTEMENTS.

Puis Lire DD-TIC-indic-reg-dep_2008_2019_2022.xls et Evolution_population_2012-2023.xlsx
Completer la base de donnée, en créant au moins 4 tables

"""


# Lire les données géographiques
geographie_df = pd.read_excel("geographie_2020.xlsx")

# Lire les données sociales et économiques
donnees_sociales_df = pd.read_excel("DD-TIC-indic-reg-dep_2008_2019_2022.xls")
donnees_population_df = pd.read_excel("Evolution_population_2012-2023.xlsx")


# Création des tables
# Table regions
table_reg = "create table public.Regions(id_reg INT CHECK (id_reg =< 94) PRIMARY KEY NOT NULL, nom_reg VARCHAR NOT NULL);"

# Table departement
table_dep = "create table public.Departements(id_dep VARCHAR(3) PRIMARY KEY NOT NULL, id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg), nom_dep VARCHAR NOT NULL);"

# Table population
table_pop = "create table public.Population(id_dep VARCHAR(3) REFERENCES Departements(id_dep) NOT NULL, annee INT CHECK (annee =< 2024) NOT NULL, nombre_personnes BIGINT NOT NULL, pourcentage_inondation FLOAT CHECK (pourcentage_inondation =< 100), pourcentage_diplome FLOAT CHECK (pourcentage_diplome =< 100), taux_activité FLOAT CHECK (taux_activité =< 100));"

# Table Effort Recherche (ER)
table_ER = "create table public.EffortRecherche(id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg) NOT NULL, annee INT CHECK (annee =< 2024) NOT NULL, pourcentage_effort FLOAT CHECK (pourcentage_effort =< 100) NOT NULL, pourcentage_plus_7_min FLOAT CHECK (pourcentage_plus_7_min =< 100))"

# Table Competences numeriques (CN)
table_CN = "create table public.CompetencesNumeriques(id_reg INT CHECK (id_reg =< 94) REFERENCES Regions(id_reg) NOT NULL, taux FLOAT CHECK (taux =< 100), intensite VARCHAR CONSTRAINT intensite CHECK(intensite = "fort" or intensite = "quotidienne" or intensite = "sans") NOT NULL)"
