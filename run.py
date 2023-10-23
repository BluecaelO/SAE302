## les module flask
from flask import Flask, render_template,request,redirect,url_for,flash,session,escape
## module personnel
from package.db_config import *
## autre module
import secrets
from  package.encryption import *


app = Flask(__name__)

app.secret_key = secrets.token_hex()

# On définit la route principal de notre serveur et la fonction in index() sera la fonction qui sera exécuter lorqsue le client accèdera à la route.
@app.route("/", methods=["GET", "POST"])
def index():
    # Les deux lignes suivantes sont à titre indicatif et servent pour le débogage
    print(session.get("login"))  # Affiche la valeur de la variable de session "login"
    print(session.get("user"))  # Affiche la valeur de la variable de session "user"

    # On teste si les variables de session sont bien configurées, sinon l'utilisateur est redirigé vers la page de login
    if session.get("login") == True:
        pwd_list = get_pwd_list()  # Appelle la fonction get_pwd_list() pour obtenir une liste de mots de passe
        return render_template("index.html", pwd_list=pwd_list, user_name=session.get("user"))
        # Rend le template "index.html" en passant la liste de mots de passe et le nom d'utilisateur au template

    elif session.get("login") == False or session.get("login") == None:
        session["user"] = None  # Définit la variable de session "user" à None
        return redirect(url_for("login"))  # Redirige l'utilisateur vers la route "login"

    else:
        return redirect(url_for("login"))  # Redirige l'utilisateur vers la route "login" (dans tous les autres cas)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")
     # Lorsque l'utilisateur essaie d'accéder à une route qui n'existe pas, cette fonction sera appelée pour gérer l'erreur 404.

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("login") == True:
        close_db()
    # Si la variable de session 'login' est définie à True, cela signifie que l'utilisateur est déjà connecté.
    # Nous fermons donc la connexion à la base de données pour éviter une erreur potentielle.


    session["login"] = False
    session["user"] = None
    session["password"] = None
    # Nous initialisons les variables de session 'login', 'user' et 'password' à False, None et None respectivement.
    # Cela nous permet de contrôler l'accès aux autres pages qui peuvent contenir des informations sensibles.


    if request.method == "POST" and "user" in request.form and "password" in request.form:
        # Vérifier si la méthode de requête est POST et si les champs de formulaire 'user' et 'password' sont présents dans les données du formulaire de la requête
        # cela permet d'éviter des utilisation de controler l'utilisation de cette page

        if escape(request.form["user"]) == "postgres" or escape(request.form["user"]) == "root":
            flash("Impossible de se connecter à la base de données")
            return redirect(url_for("login"))
        # Si le nom d'utilisateur saisi est "postgres" ou "root", on empêche la connexion.
        # Pour des raisons de sécurité, nous affichons un message d'erreur et redirigeons l'utilisateur vers la page de connexion.
        # En utilisant ces identifiants, l'utilisateur pourrait accéder à l'ensemble des tables de la base de données.
        # Nous forçons donc les utilisateurs à se connecter avec d'autres identifiants, qui leur permettront seulement de consulter les tables dont ils sont propriétaires.

        if connexion_db(escape(request.form["user"]), escape(request.form["password"])) == False:
            return redirect(url_for("login"))
        # Si la connexion à la base de données en utilisant le nom d'utilisateur et le mot de passe saisis échoue, rediriger l'utilisateur vers la page de connexion

        else:
            session["user"] = escape(request.form["user"])
            session["login"] = True
            session["password"] = escape(request.form["password"])
            # Définir les variables de session 'user', 'login' et 'password' avec les valeurs saisies
            #garce à cela on autorise k'utilisateur à accéder aux autres pages

            return redirect(url_for("index"))
            # Rediriger l'utilisateur vers la page d'accueil

    else:
        return render_template("login.html")
        # Si la méthode de requête n'est pas POST ou si les champs de formulaire 'user' et 'password' ne sont pas présents, afficher le template login.html

    
@app.route("/register",methods=["GET", "POST"])
def register():
    session["login"] = False
    session["user"] = None
    # on procède de la mème manière que pour la route qui revoi la page de login
    
    if request.method == "POST" and "user" in request.form and "password1" in request.form and "password2" in request.form:
        user = escape(request.form["user"])
        password1 = escape(request.form["password1"])
        password2 = escape(request.form["password2"])

        # Pour s'assurer de l'utilisation de la page on s'assure de la manière dont elle est utilisé
        
        if user == "":
            flash("We need a user name")
            return render_template("register.html")
        # permet de vérifier que l'utilisateur rentre un nom d'utilisateur

        if password1 == "":
            flash("We need a password")
            return render_template("register.html")
        # permet de vérifier que l'utilisateur rentre un mot de passe
        
        if password1 != password2:
            flash("Passwords not corresponding")
            return render_template("register.html")
        # permet de vérifier que le mot de passe est le même su le input "password1" et "password2"
        
        if connexion_db("postgres", "root") == False:
            return render_template("register.html")
        # permet de débuter une connexion avec l'utilisateur "postgres" qui est un administrateur.
        # On doit ce connecter avec un utilisateur car dans la configuration de les autres utilisateur n'ont pas les droits nécésaire pour ajouter des utilisateurs.
        
        if creat_user(user, password1) == False:
            close_db()
            flash("Unable to register the User")
            return render_template("register.html")
        # Ici on vérifie que la fonction creat_user() à bien fonctionner.
        # la fonction creat_user() retourne TRUE ou FALSE.
        # s'il retourne FALSE on affiche un message d'erreur
        # si c'est TRUE, on poursuit le code
                
        close_db()
        return redirect(url_for("login"))
        # ici on ne doit pas laisser la connexion root ouvert. Cela peut engendrer des problèmes de sécurité.
        # Puis on redirige l'utilisateur ves la page de login
    
    return render_template("register.html")
    # Si aucun des test n'est concluant, on renvoie la page register


# ici on prévoit la focntion pour la route "add_password"
@app.route("/add_password",methods=["GET","POST"])
def add_password():
    if not session.get("login"):
        return redirect(url_for("login"))
    # On vérifie si la session est bien set-up ou pas
    # si elle est set-up on poursuit le code
    # dans le cas contraire en renvoie l'utilisateur sur le login
    
    if request.method == "POST": 
        pass_name = escape(request.form.get('pass_name'))
        password = escape(request.form.get('password'))
        login = escape(request.form.get('pass_login'))
        site = escape(request.form.get('pass_url'))
        fav = escape(request.form.get('pass_favorite'))
        # On vérifie que la méthode est un POST cela permet de faire la distinction entre la entre le traitement du forme et le le simple fait d'aller sur la page
        
        key = derive_key(session.get("password"))
        password = encrypt_AES_CBC_256(key,password)
        #Pour éviter que la base de donné stock les ionformations en claire nous devons au minimum chiffrer le mot de passe
        

        if fav == "None":
            fav = "0"
        #Ici on est obliger de modier la valeur de la variable fav.
        #Car lorsqu'on envoie le formulaire et que 'pass_favorite' n'est pas cocher la valeur de ce dedrnier est à NONE.
        #Et la colonne de la table ne prend que les valeur de type Bite soit O ou 1
        
        if not pass_name:
            flash("We need a password name")
            return render_template("add_password.html")
        
        print("1")

        if not password:
            flash("We need a password")
            return render_template("add_password.html")
        
        print("2")

        # Pour ces deux tests, on vérifie si l'utilisateur rentre bien un nom de mot de passe et un mot de passe
        # les prints on juste pour but le débug.
        
        print(pass_name, password, login, site)
        
        if add_password_to_db(pass_name, password, login, site, fav):
            print("Ok add password")
            return redirect(url_for("index"))
            # si la focntion add_password c'est bien passé on retourn sur la page index
            
        else:
            print("else render")
            return render_template("add_password.html")
            # dans le cas contraire il nous redonne la page add_passwordp por réhitérer en cas d'érreur
            
    print("Return add_password.html")
    return render_template("add_password.html")
    # Ci tous les teste on échoué il nous redonne la page add_password

# ici on rajoute le chemin pour search
# ce chemin n'est pas directment accéssible à l'utilisateur via l'url
@app.route("/search",methods=["POST","GET"])
def search():
    if session.get("login") == True:
        # comme pour le rest du code on vérifie toujours si l'utilisateur est connecté
        if request.method == "POST" and "value" in request.args:
            value = escape(request.args.get("value"))
            pwd_list = get_pwd_list_search(value)
            return render_template("search.html", pwd_list=pwd_list)  
            # Si la requête respect les conditions, on récupère l'élément value dans l'URL pour l'utiliser comme paramètre de la fonction get_pwd_list_search()
            # cette fonction permet de faire une recherche approximative d'un mot de passe dans la base de données
        


        elif request.method == "POST" and "fav" in request.args:
            fav = request.args.get("fav")
            pwd_list = get_pwd_list_search_fav()
            return render_template("search.html", pwd_list=pwd_list)
            # On fait la même chose que précédemment sauf que cette fois, si on récupère l'élément fav et on recherche tous les éléments ou fav=1


        else:
            return "no results"
            # si il ne trouve aucun résultat il retoun "no results"
        
        
        
        '''
        elif request.method == "POST" and "category" in request.args:
            category = request.args.get("category")
            pwd_list = get_pwd_list_search_category(value)
            return render_template("search.html", pwd_list=pwd_list)
        '''
        # On a aussi essayer d'implémenter un system de classement par catégorie
        # par manque de temps on préféré nous concentrer sur les fonctionnalités essentiels
        
    else:
        return "no results"
        # si la session n'est pas set-up on va juste afficher "no results"
        # le contenu de la page search est destiner à être affiché dans l'index grâce à AJAX.
        # Donc pour éviter qu'on se retrouve avec la fenêtre login dans le code de la page index, on a décidé d'afficher un "no results"
    
# ici on rajoute le chemin pour fil_infos
# ce chemin n'est pas directment accéssible à l'utilisateur via l'url
@app.route("/fill_infos",methods=["POST"])
def fill_infos():
    if session.get("login") == True:
        if request.method == "POST" and "pass_name" in request.args:
            pass_name = escape(request.args.get("pass_name"))
            pwd = get_password(pass_name)
            key = derive_key(session.get("password"))

            tab=[] 
            for i in pwd:
                tab.append(i)
            # le test à la même utilité que précédament
            # ici on doit s'assurer de déchiffrer le mot de la DB
            #, mais le rpoblème, c'est que la variable pwd est un tuple et non un tableau.
            # Ceci pose problème, car la fonciton decrypt_AES_CBC_256() ne peut pas traiter des tuples
            # On doit créer un nouveau tableau et ont l'incrément en parcourant pwd

            tab[2] = decrypt_AES_CBC_256(key,tab[2])
            # On décrypte la valeut à l'index 2. Cela correspond à l'emplacement du mot de passe dans la table.
            return render_template("fill_infos.html", pwd=tab)  
            # Lorsque qu'on retourne la page fill_infos on retourne aussi la variable pwd qui est égale à tab
            # cela va nous permettre d'utiliser des variables avec jinja dans le code html.
            # On peut donc remplir la page avec la variabe pwd

        else:
            return "no results"
        
    else:
        return "no results"
    


# ici on rajoute le chemin pour passwords_generator
@app.route("/passwords_generator",methods=["GET","POST"])
def passwords_generator():
    if not session.get("login"):
        return redirect(url_for("login"))
    
    return render_template("passwords_gen.html")
    # Dans cette focntion on ne fait rien de spécial.
    # on vérifie si l'utilisateur c'est bien loguer correctement 
    # ci c'est le cas, on peut retourner la page passwords_gen.html





# ici on rajoute le chemin pour edit_password
# cette partie était l'une des plus compliquées, car le code devait faire la distinction entre :
# le nouveau pass_name définit par l'utilisateur
# et l'ancien pass_name qui est stocké dans la base de données.
@app.route("/edit_password", methods=["GET", "POST"])
def edit_password():
    if not session.get("login") and not session.get("user"):
        return redirect(url_for("login"))

    pass_info = None

    if request.method == "GET":
        # ce test permet de vérifier si l'utilisateur à voulu exécuter le formulaire de la page ou simplement accéder à la page
        if "pass_name" in request.args:
            # donc si la requête est un requête de type GET et si elle contient l'arguement "pass_name" on éxécute les commande suivantes
            print("L'identifiant du mot de passe est récupéré")
            pass_info = get_password(escape(request.args.get("pass_name")))

            key = derive_key(session.get("password"))

            tab=[] 
            for i in pass_info:
                tab.append(i)


            tab[2] = decrypt_AES_CBC_256(key,tab[2])

            # Ici on fait la même étape que pour le fill_infos.
            # on récupère les données et on décrypte le mot de passe.
            # à la fin, on doit retourner le page fill_ionfos ainsi que la variable pass_infos qui est égale à tab pour pré remplie nos champs avec jinja.
            if not pass_info:
                return redirect(url_for("index"))
        else:
            flash("Pass name not found")
            return redirect(url_for("index"))
            # si le mot de passe n'est pas trouvé, on envoie un message qui dit qu'on ne trouve pas le pass_name

    if request.method == "POST":
        print("Le formulaire a été pris en compte")
        new_pass_name = escape(request.form.get('new_pass_name'))
        new_password = escape(request.form.get('new_password'))
        new_login = escape(request.form.get('new_pass_login'))
        new_site = escape(request.form.get('new_pass_url'))
        new_fav = escape(request.form.get('new_pass_favorite'))
        pass_name = escape(request.form.get("pass_name"))
        pass_info = get_password(pass_name)
        print(pass_info)

        key = derive_key(session.get("password"))
        new_password = encrypt_AES_CBC_256(key,new_password)

        # la condition que vous pouvez voir ci-dessus permet de vérifier s'il s'agit d'une requête POST.
        # car le formulaire a été configuré pour envoyé de requête post

        if new_fav == "None":
            new_fav = "0"

        if not pass_info:
                return redirect(url_for("index"))

        if not new_pass_name:
            flash("We need a password name")
            return render_template("edit_password.html", pass_info=tab)

        if not new_password:
            flash("We need a password")
            return render_template("edit_password.html", pass_info=tab)

        # le reste des conditions que vous voyez ci-dessus ont la même utilité que pour la fonction add_password()

        print(new_pass_name, new_login, new_password , new_site)
        print("Le nom du mot de passe actuel = " + pass_name)
        # les prints servent aux débug

        if not edit_password_to_db(new_pass_name, new_login,new_password ,new_site, new_fav, pass_name):
            return render_template("edit_password.html", pass_info=tab)
            # si la fonction edit_password_to_db() à échouer on retourne la page edit_password.html pour réitérer la procédure.
            # c'est l'une des raison pour laquelle il était compliqué de faire la fonction edit_password().
            # car si la fonction edit_password_to_db() on doit pouvoir récupérer l'information pass_name par la méthode POST.
            # sachant que la méthode Post est générée par le formulaire.
            # On a donc décidé de faire un input caché pour envoyé le pass_name.
            # Pour pouvoir relancer un requête SQL afin d'avoir toutes les onformations du mot de pass

        return redirect(url_for("index"))
        # ici si le mot de passe a bien été changé on redirege l'utilisateur vers la page index

    return render_template("edit_password.html", pass_info=tab)
    # Ici comme tous à échouer on retourn la page edit_password.html qui sera remplie à l'aide de pass_infos

# ici on rajoute le chemin pour del_password
@app.route("/del_password", methods=["POST"])
def del_password():
    if session.get("login") == True:
        #on fait la vérifivcation habituel
        pass_name = escape(request.args.get("pass_name"))
        # On récupère le "pass_name"
        # cela va nous permettre de préciser l'élément à supprimer.
        del_password_into_db(pass_name)
        # on supprime l'élément
        if request.method == "POST" and "pass_name"  in request.args:
            value = ""
            pwd_list = get_pwd_list_search(value)
            return render_template("search.html", pwd_list=pwd_list) 
            # On récupère la liste des mot de passe mise à jour pour pouvoir l'afficher;
            # Cela prmet d'éviter de recharger la page
        
    return "No results"
    # ci l'utilisateur n'est pas loguer on affiche "no results"
    

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080,ssl_context=('/home/server/SAE302/cert.pem', '/home/server/SAE302/priv_key.pem'))
