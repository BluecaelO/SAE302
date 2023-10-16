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
    'host': '192.168.178.58',
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
    
def creat_user(user,password):
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

            
            CREATE TABLE IF NOT EXISTS {user+"_vault"} (
                pass_name VARCHAR(255) PRIMARY KEY,
                login VARCHAR(255),
                password VARCHAR(255),
                site VARCHAR(255)
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



def get_pwd_list():
    global conn
    # Récupérer le nom de l'utilisateur à partir de la session
    user = session.get('user')
    # Vérifier si l'utilisateur est connecté
    if user:
        try:
            cursor = conn.cursor()
            query = f"SELECT pass_name, site FROM {user + '_vault'}"

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
    


def add_password_to_db(pass_name, password, login, site):
    print("deuxième phase")
    global conn
    user = session.get('user')
    if user:
        try:
            cursor = conn.cursor()
            
            # Vérifier si le mot de passe existe déjà dans la base de données
            query = f"SELECT pass_name FROM public.{user + '_vault'} WHERE pass_name = '{pass_name}'"
            cursor.execute(query)
            existing_password = cursor.fetchone()
            
            if existing_password:
                flash("The password already exists")
                return False
            
            # Insérer les données dans la base de données
            query = f"INSERT INTO public.{user + '_vault'} (pass_name, login, password, site) VALUES ('{pass_name}', '{login}', '{password}', '{site}')"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            print("Insertion réussie")
            return True
        except psycopg2.Error as e:
            flash("Error: we can't add the password")
            print("Error SQL:", e)
            return False
#url de test
#http://127.0.0.1:5000/add_password?pass_name=pass_name&password=password&login=login&site=site

        