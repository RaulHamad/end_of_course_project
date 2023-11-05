from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template,url_for, request,redirect,flash
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,RadioField



from models import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/luxurywheels.db'
app.config["SECRET_KEY"] = '123456'
db = SQLAlchemy()
bcrypt = Bcrypt(app)
db.init_app(app)


class Formregister(FlaskForm):

    username = StringField()
    user_email = StringField()
    user_password = PasswordField()
    user_check_password = PasswordField()
    user_category = RadioField(choices=[('value_1','Gold'),('value_2','Silver'),('value_3','Economy')],default='value_1')
    submit = SubmitField()


@app.route("/")
@app.route("/index")
def page_index():

    return render_template("index.html")

@app.route("/register", methods=["GET","POST"])
def page_register():
    form = Formregister()
    if form.validate_on_submit():

        user1 = User(
            name = form.username.data,
            email = form.user_email.data,
            password = form.user_password.data,

        )
        db.session.add(user1)
        db.session.commit()

        return redirect(url_for('page_index'))

    return render_template("register.html", form=form)









if __name__ == "__main__":
    app.run(debug=True)