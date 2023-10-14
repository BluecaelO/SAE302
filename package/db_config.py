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
    'host': '192.168.251.58',
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

        # Définir la requête SQL pour créer une table en fonction du nom de l'utilisateur
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

            
            CREATE TABLE IF NOT EXISTS "{user+"_vault"}" (
                pass_name VARCHAR(255) PRIMARY KEY,
                login VARCHAR(255),
                password VARCHAR(255),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            );
        

            ALTER TABLE IF EXISTS "{user + "_vault"}"
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