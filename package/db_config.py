## module nécéssaire
import psycopg2
from flask import *

conn=None

## Connexion DB
def connexion_db(user,pwd):
    global conn

    # Nous créons ici un dictionnaire qui va se charger de stocker les informations de connexion à la base de données postgres SQL
    db_config = { 
    'dbname': 'postgres',
    'user': user,
    'password': pwd,
    'host': '127.0.0.1',
    'port': '5432'
    }
    try:
        # On essaie de se connecter et on print dans le terminal "Connexion réussie" si on arrive à se connecter
        conn = psycopg2.connect(**db_config) 
        print("Connexion réussie")
        return True
    except psycopg2.OperationalError as e:
        # En cas d'échec de connexion à la db on affiche sur la page le message "Unable to connect to the DB"
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

            # On crée ici la table qui va servir à contenir les mots de passe des utilisateurs 
            CREATE TABLE IF NOT EXISTS {user+"_vault"} (
                pass_name VARCHAR(255) PRIMARY KEY,
                login VARCHAR(255),
                password VARCHAR(255),
                site VARCHAR(255),
                favorite BIT
            );


            ALTER TABLE IF EXISTS "{user + "_vault"}" OWNER to "{user}";

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
            # permet de récupérer toutes les données dans le coffre personnel de l'utilisateur. 
            # Cette requête est utilisée notamment dans la grande majorité des pages lorsque l'on souhaite récupérer des données liées aux mots de passe
            cursor = conn.cursor()
            query = f"SELECT pass_name, site, favorite FROM {user + '_vault'}"

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
    

def add_password_to_db(pass_name, password, login, site, fav):
    print("deuxième phase")
    global conn
    user = session.get('user')
    if user:
        try:
            cursor = conn.cursor()
            
            # Vérifier si le mot de passe existe déjà dans la base de données (utiliser dans la page add_pasword)
            query = f"SELECT pass_name FROM public.{user + '_vault'} WHERE pass_name = '{pass_name}'"
            cursor.execute(query)
            existing_password = cursor.fetchone()
            
            if existing_password:
                flash("The password already exists")
                return False
            
            # Insérer les données dans la base de données
            query = f"INSERT INTO public.{user + '_vault'} (pass_name, login, password, site, favorite) VALUES ('{pass_name}', '{login}', '{password}', '{site}', '{fav}')"
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

def get_pwd_list_search(value):
    global conn
    # Récupérer le nom de l'utilisateur à partir de la session
    user = session.get('user')
    # Vérifier si l'utilisateur est connecté
    if user:
        try:
            # Cette requête permet de récupérer les infos relatives au mot de passe que l'on recherche à partir de "value" qui provient de ce que l'on entre dans la barre de recherche 
            cursor = conn.cursor()
            query = f"SELECT pass_name, site, favorite FROM {user + '_vault'} WHERE pass_name LIKE '%{value}%'"

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
    
def get_pwd_list_search_fav():
    global conn
    # Récupérer le nom de l'utilisateur à partir de la session
    user = session.get('user')
    # Vérifier si l'utilisateur est connecté
    if user:
        try:
            cursor = conn.cursor()
            # Cette requête recherche les mots de passe favoris en regardant si l'attribue "favorite" vaut 1
            query = f"SELECT pass_name, site, favorite FROM {user + '_vault'} WHERE favorite = '1'"

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
'''
def get_pwd_list_search_category(category):
    global conn
    # Récupérer le nom de l'utilisateur à partir de la session
    user = session.get('user')
    # Vérifier si l'utilisateur est connecté
    if user:
        try:
            cursor = conn.cursor()
            query = f"SELECT pass_name, site FROM {user + '_vault'} WHERE category LIKE '{category}'"

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
#url de test
#http://127.0.0.1:5000/search?value=Linkedin
'''

'''
def get_category_list():
    global conn
    # Récupérer le nom de l'utilisateur à partir de la session
    user = session.get('user')
    login = session.get('login')

    print("get_category_list")
    # Vérifier si l'utilisateur est connecté
    if user and login==True:
        try:
            cursor = conn.cursor()
            query = f"SELECT * FROM {user + '_category'}"

            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            # Retourner les données
            print("success data reception")
            print(rows)
            return rows

        except psycopg2.Error as error:
            print("Erreur SQL: ", error)
            return "Erreur lors de la récupération des données"

    else:
        return "Utilisateur non connecté"
'''  

def get_password(value):
    global conn
    # Récupérer le nom de l'utilisateur à partir de la session
    user = session.get('user')
    # Vérifier si l'utilisateur est connecté
    if user:
        try:
            cursor = conn.cursor()
            # Ici on récupère le mot de passe de l'utilisateur à partir du nom du mot de passe
            query = f"SELECT pass_name, login,password,site,favorite FROM {user + '_vault'} WHERE pass_name = '{value}'"

            cursor.execute(query)
            rows = cursor.fetchone()
            cursor.close()
            
            # Retourner les données
            return rows

        except psycopg2.Error as error:
            print("Erreur SQL: ", error)
            return "Erreur lors de la récupération des données"

    else:
        return "Utilisateur non connecté"
    


def edit_password_to_db(new_pass_name, new_login, new_password, new_site,new_favorite, pass_name):
    print("deuxième phase")
    print(pass_name, new_pass_name)
    global conn
    user = session.get('user')
    if user:
        try:
            cursor = conn.cursor()
            # Ici on modifie les informations d'un mot de passe (pour la page edit password)
            query = f"UPDATE public.{user + '_vault'} SET pass_name = '{new_pass_name}', login = '{new_login}', password = '{new_password}', site = '{new_site}', favorite = '{new_favorite}' WHERE pass_name = '{pass_name}'"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            print("Insertion réussie")
            return True
        
        except psycopg2.Error as e:
            flash("Error: we can't add the password")
            print("Error SQL:", e)
            return False
        

def del_password_into_db(pass_name):
    global conn

    user = session.get('user')

    if user:
        try:
            cursor = conn.cursor()
            # Cette requête est utilisée pour le bouton de la page index afin de supprimer le mot de passe sélectionné ici on retrouve le mot de passe avec son nom et on le supprime
            query = f"DELETE FROM public.{user + '_vault'} WHERE pass_name = '{pass_name}';"
            cursor.execute(query)
            conn.commit()
            cursor.close()
            print("Suppression réussie")
            return True
        
        except psycopg2.Error as e:
            flash("Error: we can't delete the password")
            print("Error SQL:", e)
            return False    


