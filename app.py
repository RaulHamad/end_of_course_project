from flask import Flask, render_template,url_for, request,redirect
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/luxury.db'
db = SQLAlchemy()
db.init_app(app)




@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")





if __name__ == "__main__":
    app.run(debug=True)