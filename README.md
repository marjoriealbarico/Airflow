LIEN REPO GIT

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

PARAMÈTRAGES AIRFLOW CONNEXION :
Connection Id  = postgres_connexion
Connection Type = Postgres
Host = host.docker.internal
Schema = airflow
login = airflow
mdp = airflow
Port = 5435


PARAMÈTRAGES POSTGRESQL (dbeaver):
host = localhost
port = 5435
database = airflow
authentification = databse native
nom d'utiisateur = airflow
mdp = airflow

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

STRUCTURE BASE DE DONNÉES:

departments_region (num_dep(PK) , dep_name , region_name )


tranche_age (code (PK) , tranches_age_min , tranches_age_max )

urgences_covid ( id (PK) , dep (FK departments_region.num_dep) , date_de_passage , sursaud_cl_age_corona (FK tranche_age.code) , nbre_pass_corona , nbre_pass_tot , nbre_hospit_corona , nbre_pass_corona_h , nbre_pass_corona_f , nbre_pass_tot_h , nbre_pass_tot_f , nbre_hospit_corona_h , nbre_hospit_corona_f )

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

STRUCTURE DU DOSSIER
data : contient toutes les sources de données
dag : contient dissier sql et le fichier dag pour airflow
    sql : contient tous les fichiers sql

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

EXECUTION DE DAG :
Une fois la connexion est établie, vous trouverez le dag "ETL_projet" dans la liste.
Activez le buoton et cliquez pour voir les détails de dag
Cliquez sur le buoton ▶️ qui se trouve en haut à droit pour lancer le dag
Si vous cliquez sur l'onglet graph, vous trouverez les diférentes étapes
Pour la création de table, nous avons choisi de faire premièrement les table tranche_age et departments_region. Ensuite, la table urgences_covid car il y a des clé étrangères qui sont référencées aux 2 premières tables.
Une fois le dag est terminé, vous allez voir qu'ils sont tous en "success" en vert
Vous pouvez vérifier dans votre base de donnnées si les données sont bien importé

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Pour répondre aux questions d'objectifs, vous pouvez lancez les requêtes dans votre base de données
