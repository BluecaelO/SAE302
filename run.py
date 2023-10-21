## les module flask
from flask import Flask, render_template,request,redirect,url_for,flash,session,escape
## module personnel
from package.db_config import *
## autre module
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex()

@app.route("/", methods=["GET", "POST"])
def index():
    print(session.get("login"))
    print(session.get("user"))
    if session.get("login") == True:
        pwd_list=get_pwd_list()
        return render_template("index.html",pwd_list=pwd_list,user_name = session.get("user"))
    elif session.get("login") == False or session.get("login") == None:
            session["user"] = None
            return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("login") == True:
        close_db()
    session["login"] = False
    session["user"] = None
    if request.method == "POST" and "user" in request.form and "password" in request.form:
        if connexion_db(request.form["user"], request.form["password"]) == False:
            return redirect(url_for("login"))
        else:
            session["user"] = request.form["user"]
            session["login"] = True
            return redirect(url_for("index"))
    else:
        return render_template("login.html")
    
@app.route("/register",methods=["GET", "POST"])
def register():
    session["login"] = False
    session["user"] = None
    
    if request.method == "POST" and "user" in request.form and "password1" in request.form and "password2" in request.form:
        user = escape(request.form["user"])
        password1 = escape(request.form["password1"])
        password2 = escape(request.form["password2"])
        
        if user == "":
            flash("We need a user name")
            return render_template("register.html")

        if password1 == "":
            flash("We need a password")
            return render_template("register.html")
        
        if password1 != password2:
            flash("Passwords not corresponding")
            return render_template("register.html")
        
        if connexion_db("root", "root") == False:
            return render_template("register.html")
        
        if creat_user(user, password1) == False:
            close_db()
            flash("Unable to register the User")
            return render_template("register.html")
        
        close_db()
        return redirect(url_for("login"))
    
    return render_template("register.html")

@app.route("/add_password",methods=["GET","POST"])
def add_password():
    if not session.get("login"):
        return redirect(url_for("login"))
    
    category_list = get_category_list()
    
    if request.method == "POST":
        pass_name = escape(request.form.get('pass_name'))
        password = escape(request.form.get('password'))
        login = escape(request.form.get('pass_login'))
        site = escape(request.form.get('pass_url'))
        category = escape(request.form.get('pass_category'))
        
        if not pass_name:
            flash("We need a password name")
            return render_template("add_password.html", category_list=category_list)
        
        if not password:
            flash("We need a password")
            return render_template("add_password.html", category_list=category_list)
        
        print(pass_name, password, login, site)
        
        if add_password_to_db(pass_name, password, login, site, category):
            return redirect(url_for("index"))
        else:
            return render_template("add_password.html", category_list=category_list)
    
    return render_template("add_password.html", category_list=category_list)

@app.route("/search",methods=["POST"])
def search():
    if session.get("login") == True:
        if request.method == "POST" and "value" in request.args:
            value = escape(request.args.get("value"))
            pwd_list = get_pwd_list_search(value)
            return render_template("search.html", pwd_list=pwd_list)  
        
        elif request.method == "POST" and "fav" in request.args:
            fav = request.args.get("fav")
            pwd_list = get_pwd_list_search_fav()
            return render_template("search.html", pwd_list=pwd_list)


        else:
            return "no results"
        
        
        
        '''
        elif request.method == "POST" and "category" in request.args:
            category = request.args.get("category")
            pwd_list = get_pwd_list_search_category(value)
            return render_template("search.html", pwd_list=pwd_list)
        '''
        
    else:
        return "no results"
    



@app.route("/passwords_generator",methods=["GET","POST"])
def passwords_generator():
    if not session.get("login"):
        return redirect(url_for("login"))
    
    return render_template("passwords_gen.html")

if __name__ == '__main__':
    app.run(debug=True)


