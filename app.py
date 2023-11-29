from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, session

from models import *
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/luxurywheels.db'
app.config["SECRET_KEY"] = '123456'
db = SQLAlchemy()
db.init_app(app)


# bcrypt = Bcrypt(app)


@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def page_index():
    # user_all = db.session.query(User).all()
    if request.method == 'POST':
        email = request.form['email_login'].lower().strip()
        password = request.form['password_login']

        user = db.session.query(User).filter(User.email == email and User.password == password).first()

        if user == None:
            msg_error = f'Email does not exist. Please register'
            print('error email')
            return render_template('index.html', msg_error=msg_error)
        elif check_password_hash(user.password,password) is False:
            msg_error = f'Password does not exist. Please register'
            print('error pass')
            return render_template('index.html', msg_error=msg_error)

        else:
            print('ok')

            return redirect(url_for('rent_car'))

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def page_register():
    cat_all = db.session.query(Category).all()

    if request.method == 'POST':
        user = request.form['name_login'].lower().strip()
        email = request.form['email_login'].lower().strip()
        password = request.form['password_login'].lower().strip()
        check_password = request.form['check_password_login'].lower().strip()
        categ = request.form['category']
        result = db.session.query(Category).filter(Category.id == int(categ)).first()
        check_email = db.session.query(User).filter(User.email == email).first()
        pass_cryp = generate_password_hash(password, method='pbkdf2:sha256')

        if result != None:
            if check_email:

                error = f'E-mail already registered!!'
                return render_template("register.html", error=error, cat_all=cat_all)
            elif password != check_password:
                error = f'Try password again!!'
                return render_template("register.html", error=error, cat_all=cat_all)

            else:

                user1 = User(name=user, email=email, password=pass_cryp,
                             categories_id=int(categ))
                db.session.add(user1)
                db.session.commit()
                create = f'Client Registered'
                return render_template('index.html', create=create, cat_all=cat_all)

    return render_template("register.html", cat_all=cat_all)


@app.route('/rent_car', methods=["GET", "POST"])
def rent_car():
    return render_template('rent.html')


if __name__ == "__main__":
    app.run(debug=True)
