## les module flask
from flask import Flask, render_template,request,redirect,url_for,flash,session
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
        return render_template("index.html",pwd_list=pwd_list)
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
        if request.form["user"]=="":
            flash("We need a user name")
            return render_template("register.html")

        if request.form["password1"]=="":
            flash("We need a password")
            return render_template("register.html")
        
        if request.form["password1"]!=request.form["password2"]:
            flash("Passwords not correspondig")
            return render_template("register.html")
        
        if connexion_db("root","root")== False:
            return render_template("register.html")
        
        if creat_user(request.form["user"],request.form["password1"])==False:
            close_db()
            flash("Unable to register the User")
            return render_template("register.html")
        
        close_db()
        return redirect(url_for("login"))
    return render_template("register.html") 


@app.route("/add_password",methods=["GET","POST"])
def add_password():
    if session.get("login") == True:
        if request.method == "POST" and "pass_name" in request.form and "password" in request.form and "pass_login" in request.form and "pass_url" in request.form:
            pass_name = request.form.get('pass_name')
            password = request.form.get('password')
            login = request.form.get('pass_login')
            site = request.form.get('pass_url')
            if request.form["pass_name"]=="":
                flash("We need a password name")
                return render_template("add_password.html")
            if request.form["password"]=="":
                flash("We need a password")
                return render_template("add_password.html")
            
            print(pass_name,password,login,site)
            if add_password_to_db(pass_name,password,login,site):
                return redirect(url_for("index"))
            else:
                return render_template("add_password.html")
        else:
            return render_template("add_password.html")
    else:
        return redirect(url_for("login"))

@app.route("/search",methods=["GET","POST"])
def search():
    if session.get("login") == True:
        if request.method == "POST" and "value" in request.args:
            value = request.args.get("value")
            pwd_list = get_pwd_list_search(value)
            return render_template("search.html", pwd_list=pwd_list)
        else:
            return "no results"
    else:
        return "no results"

if __name__ == '__main__':
    app.run(debug=True)




