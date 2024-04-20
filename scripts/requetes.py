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
