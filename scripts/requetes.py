"""
TODO : 

Afficher la liste des régions où le taux de la population habitant en zone inondable était supérieure a 10% en 2013, classées du plus fort taux au plus faible.

Quelle est la variation de l'effort de recherche et développement entre 2010 et 2014 dans les régions dont moins de 70% de la population a une utilisation quotidienne d'internet en 2019? Afficher aussi le taux d'activité en 2019 pour ces régions.

Quels sont les départements dont moins du quart la population de la région avait un des compétences numériques fortes en 2019 ? Afficher aussi l'évolution de la part des jeunes diplôme entre 2009 et 2014 pour ces départements.

Quelle est l'estimation de population en 2020 de tous les départements où l'absence d'équipement internet est supérieure ou égale a 12.5% (en 2019).

Quelle était la part de la population ayant une utilisation quotidienne d'internet dans les régions où le taux d'activité était >75% en 2019 et où la Part de la population éloignée de plus de 7 mn des services de santé de proximité était de moins de 5% en 2021.

"""
import pandas as pd
import psycopg2 
import psycopg2.extras
from creation_bdd import connection, execute_command

def execute_query(command, conn, cur):
    """
    Execute une requete 
    """
    try:
        cur.execute(query)
        rows = cur.fetchall()
        return rows
    except psycopg2.Error as e:
        cur.close()
        conn.close()
        print("Error:", e)
        return None

# Connection
conn, cur = connection("username", "password") # à remplacer par le mot de passe d’accès aux bases

# Afficher la liste des régions où le taux de la population habitant en zone inondable 
# était supérieure a 10% en 2013, classées du plus fort taux au plus faible.

Question_1 = "SELECT nom_reg FROM Regions INNER JOIN Population ON Regions.id_reg = Population.id_reg WHERE zone_inondable_2013 > 10 ORDER BY zone_inondable_2013 DESC;"
execute_command(Question_1, conn, cur)

# Quelle est la variation de l'effort de recherche et développement entre 2010 et 2014 
# dans les régions dont moins de 70% de la population a une utilisation quotidienne d'internet en 2019? 
# Afficher aussi le taux d'activité en 2019 pour ces régions.

Question_2 = "SELECT nom_reg, effort_recherche_2014 - effort_recherche_2010 AS variation_recherche, taux_activite_2019 FROM Regions INNER JOIN EffortRecherche ON Regions.id_reg = EffortRecherche.id_reg INNER JOIN Population ON Regions.id_reg = Population.id_reg WHERE taux < 70;"
execute_command(Question_2, conn, cur)

# Quels sont les départements dont moins du quart la population de la région avait un des compétences numériques fortes en 2019 ? 
# Afficher aussi l'évolution de la part des jeunes diplôme entre 2009 et 2014 pour ces départements.

Question_3 = " SELECT "

execute_command(Question_3, conn, cur)

# Quelle est l'estimation de population en 2020 de tous les départements où l'absence d'équipement internet 
# est supérieure ou égale a 12.5% (en 2019).

Question_4 = "SELECT nom_dep, estimation_pop_2020 FROM Departements INNER JOIN Population ON Departements.id_dep = Population.id_dep INNER JOIN CompetencesNumeriques ON CompetencesNumeriques.id_reg = Departements.id_reg WHERE intensite = 'sans' and taux >= 12.5;"

execute_command(Question_4, conn, cur)

# Quelle était la part de la population ayant une utilisation quotidienne d'internet dans les régions où le taux d'activité 
# était >75% en 2019 et où la Part de la population éloignée de plus de 7 mn des services de santé de proximité était de moins de 5% en 2021.

Question_5 = "SELECT"

execute_command(Question_5, conn, cur)










