from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, url_for, request, redirect, session
from datetime import datetime
from models import *
from manager import App_admin,Tk
from werkzeug.security import generate_password_hash, check_password_hash



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../database/luxurywheels.db'
app.config["SECRET_KEY"] = '123456'
db = SQLAlchemy()
db.init_app(app)




@app.route("/")
@app.route("/index", methods=["GET", "POST"])
def page_index():
    """
        session.clear() : limpar session para não acessar página de aluguel sem estar logado

        check_rents,check_vehicles,date_today : atualiza banco de dados de aluguel e veiculos.

    Aluguel finalizado retorna status False e status do veiculo altera para True.

        Request form para realizar login do usuario

    """
    session.clear()
    check_rents = db.session.query(Rent).all()
    check_vehicles = db.session.query(Vehicle).filter(Vehicle.status==False).all()
    date_today = datetime.now().date()

    for check_date in check_rents:
        if check_date.return_date == date_today:
            check_date.status_rent = False
            db.session.commit()

    for check_vehicle in check_vehicles:
        for check_date in check_rents:
            if check_date.status_rent == False and check_date.vehicle_id == check_vehicle.id:
                check_vehicle.status = True
                db.session.commit()
    if check_rents == []:
        for check_vehicle in check_vehicles:
            check_vehicle.status = True
            db.session.commit()



    if request.method == 'POST':
        email = request.form['email_login'].lower().strip()
        password = request.form['password_login']

        user = db.session.query(User).filter(User.email == email and User.password == password).first()

        if user == None:
            msg_error = f'Email does not exist. Please register'
            return render_template('index.html', msg_error=msg_error)

        elif check_password_hash(user.password,password) is False:
            msg_error = f'Password does not exist. Please register'
            print('error pass')
            return render_template('index.html', msg_error=msg_error)

        else:
            session.clear()
            session['clients_id'] =user.id

            return redirect(url_for('rent_car'))

    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def page_register():
    """
    Rota para registro do usuario e criação do objeto para o banco de dados


    """
    cat_all = db.session.query(Category).all()

    if request.method == 'POST':
        user = request.form['name_login'].strip()
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



@app.route('/rent_car/', methods=["GET", "POST"])
def rent_car():
    """
        Clients_login : verificação para limitar acesso a rota, apenas se estiver logado
        user : pesquisa para verificar o Id do cliente e realizar um filtro para identificar a categoria de cada um
        cars: usuario escolhe veiculo de acordo com sua categoria e a disponibilidades dos veiculos
        date_format_begin,date_format_end : converter str para date.


    """
    clients_login = session.get('clients_id')
    if clients_login == None:
        error_login = f'You need to login'

        return render_template('index.html',error_login=error_login)
    user = db.session.query(User).filter(User.id == clients_login).first()
    categ = db.session.query(Category).filter(Category.id == user.categories_id).first()

    if user.categories_id == 1:
        vehicle = db.session.query(Vehicle).order_by(Vehicle.name).filter(Vehicle.status == True).all()


    elif user.categories_id == 2:
        vehicle = (db.session.query(Vehicle).filter(Vehicle.category_id >= 2).filter
                   (Vehicle.status == True).order_by(Vehicle.name).all())


    else:
        vehicle = (db.session.query(Vehicle).filter(Vehicle.category_id == 3).filter
                   (Vehicle.status == True).order_by(Vehicle.name).all())

    if request.method == 'POST':

        car = request.form['cars']
        date_begin = request.form['date_begin']
        date_end = request.form['date_end']

        date_format_begin = datetime.strptime(date_begin,'%Y-%m-%d').date()
        date_format_end = datetime.strptime(date_end, '%Y-%m-%d').date()
        days = (date_format_end - date_format_begin).days
        if days < 0:
            days = ((date_format_end - date_format_begin).days) * (-1)

        price = db.session.query(Vehicle).filter(Vehicle.id == int(car)).first()
        print(date_format_begin,date_format_end)
        print(date_begin,date_end)
        total_price = (price.price_day) * days
        session['vehicle_id'] = price.id
        session['total_days'] = days
        session['date_begin'] = date_begin
        session['date_end'] = date_end





        return render_template("end_rent.html", price=price,user=user,categ=categ,
                               vehicle=vehicle,total_price=total_price,date_format_begin=date_format_begin,
                               date_format_end=date_format_end)





    return render_template("rent.html", user=user, categ=categ,vehicle=vehicle)


@app.route('/end_rent/', methods=['GET', 'POST'])
def end_rent():
    """
    Rota para exibir os dados selecionados pelo usuário e confirmação do aluguel, criando os dados na tabela rents

    :return:
    """
    clients_login = session.get('clients_id')
    vehicless = session.get('vehicle_id')
    day_sub = session.get('total_days')
    date_begin = session.get('date_begin')
    date_end = session.get('date_end')
    date_format_begin = datetime.strptime(date_begin,'%Y-%m-%d').date()
    date_format_end = datetime.strptime(date_end,'%Y-%m-%d').date()
    if clients_login == None:
        error_login = f'You need to login'

        return render_template('index.html', error_login=error_login)

    user = db.session.query(User).filter(User.id == clients_login).first()
    categ = db.session.query(Category).filter(Category.id == user.categories_id).first()
    vehicle = db.session.query(Vehicle).filter(Vehicle.id == vehicless).first()

    if vehicle != None:


            rent1 = Rent(client_id=user.id,vehicle_id=vehicle.id,pick_up_date=date_format_begin,
                         return_date=date_format_end,price_day=vehicle.price_day,status_rent=True,
                         total_price=(vehicle.price_day*day_sub))
            db.session.add(rent1)
            db.session.commit()
            vehicle.status = False
            db.session.commit()
            success = f'Successfully rented vehicle!'
            return render_template("index.html",success=success,vehicle=vehicle,categ=categ,user=user)





    return render_template("end_rent.html",vehicle=vehicle,categ=categ,user=user)



@app.route('/manager/')
def manager():
    """
    Inicializar o app administrador(será feito o app pelo tkinter)
    :return:
    """
    if __name__ == '__main__':
        root = Tk()
        app = App_admin(root)

        root.mainloop()

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
