# Introduction
## Les avantages du modèle relationnel
SQL est un langage de programmation utilisé pour gérer et manipuler des bases de données relationnelles.

Excel et les autres logiciels de gestion de données tabulaires, bien que très pratiques, présentent quelques limitations par rapport à SQL. Ils sont plus lents, ont des problèmes de portabilité, sont moins structurés et ne peuvent pas évoluer comme une base de données relationnelle. De plus, grâce au langage SQL, une infinité de requêtes peut être soumise à la base de données pour en tirer des informations détaillées.

Ainsi, lors de ce travail, nous inclurons les données de l'INSEE dans un modèle relationnel pour effectuer des requêtes sur ces dernières.
## Approche
Tout d'abord, les données seront extraites des fichiers tabulaires et inscrites dans des DataFrames pandas. Elles seront ainsi triées pour faciliter leur utilisation et nettoyées. Nous enlèverons ainsi toutes les données inutiles à nos requêtes.

Dans un second temps, nous utiliserons un module de Python pour communiquer avec une base de données PostgreSQL. Nous créerons des tables qui seront ensuite remplies.

Finalement, nous créerons des requêtes pour répondre aux questions, un script pour parcourir les tables et un module de sauvegarde des données.

# Schema de relation
Voici le schema de relation de notre base de donées comprenant 5 tables. 

# Explication sur vos choix de requêtes
## Question 1
- `SELECT r.nom_reg, s.zone_inondable_2013`: Spécifie les colonnes à sélectionner dans le résultat. `r.nom_reg` représente le nom de la région, et `s.zone_inondable_2013` représente le taux de population habitant en zone inondable en 2013.

- `FROM public.Regions r JOIN public.Social s ON r.id_reg = s.id_reg`: Indique les tables à partir desquelles les données sont sélectionnées. Nous utilisons une jointure (JOIN) pour combiner les données des tables "Regions" (aliasée en tant que "r") et "Social" (aliasée en tant que "s"). Les tables sont jointes sur la colonne "id_reg", qui représente l'ID de la région.

- `WHERE s.zone_inondable_2013 > 10`: Filtre les lignes en fonction d'une condition. Nous sélectionnons uniquement les lignes où le taux de population habitant en zone inondable en 2013 est supérieur à 10%.

- `ORDER BY s.zone_inondable_2013 DESC`: Trie les résultats par ordre décroissant du taux de population habitant en zone inondable en 2013. Cela signifie que les régions avec les taux les plus élevés apparaîtront en premier dans le résultat.

## Question 2
## Question 3
## Question 4
## Question 5

# Conclusion
