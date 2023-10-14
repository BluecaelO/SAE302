## module nécéssaire
import psycopg2
from flask import *

conn=None

## Connexion DB
def connexion_db(user,pwd):
    global conn

    db_config = { 
    'dbname': 'flask',
    'user': user,
    'password': pwd,
    'host': '192.168.38.58',
    'port': '5432'
    }
    try:
        conn = psycopg2.connect(**db_config) 
        print("Connexion réussie")
        return True
    except psycopg2.OperationalError as e:
        flash('Unable to connect to the DB!',format(e))
        print("Erreur de connexion : " + str(e))
        return False
    
def creatuser(user,password):
    global conn
    try:
        # Créer un objet curseur
        cursor = conn.cursor()

        # Définir la requête SQL pour créer une table en fonction du nom de l'utilisateur.
        query = f'''
            CREATE ROLE "{user}" WITH
            LOGIN
            NOSUPERUSER
            NOCREATEDB
            NOCREATEROLE
            NOINHERIT
            NOREPLICATION
            CONNECTION LIMIT -1
            PASSWORD '{password}';

            CREATE TABLE IF NOT EXISTS "{user + "tbl"}" (
            );

            ALTER TABLE IF EXISTS "{user + "tbl"}"
            OWNER to "{user}";
        '''
        # Execute la requête   
        cursor.execute(query)
        conn.commit()

    except psycopg2.Error as error:
        # Gérer l'erreur de manière appropriée
        print("Erreur SQL: ", error)
        return False

    finally:
        # Toujours fermer le curseur et la connexion, même en cas d'erreur
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return True
    

## Déconnexion DB
def close_db():
    global conn

    try:
        conn.close()
        conn=None
        print("Connexion ferme")
    except psycopg2.Error as e:
        print("Erreur de fermeture : " + str(e))



def get_pwd_list():
    # Récupérer le nom de l'utilisateur à partir de la session
    user = session.get('user')
    # Vérifier si l'utilisateur est connecté
    if user:
        try:
            cursor = conn.cursor()
            query = f"SELECT pwdname, pwdid FROM {user + 'tbl'}"

            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            # Retourner les données
            return rows

        except psycopg2.Error as error:
            print("Erreur SQL: ", error)
            return "Erreur lors de la récupération des données"

    else:
        return "Utilisateur non connecté"