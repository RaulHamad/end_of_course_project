from flask_sqlalchemy import SQLAlchemy

from app import db,app




class Category(db.Model):
    """
    Criação da tabela category_clients para passar que tipo de categoria o cliente se cadastrou

    categoria : Gold, Silver, Economic
    """
    __tablename__ = "category_clients"

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50),nullable=False, unique=True)
    users = db.relationship('User', backref='category', lazy=True)


class User(db.Model):
    """
      Criação da tabela User para cadastro dos clientes

      id do cliente
      nome do cliente
      email do cliente
      senha do cliente
      categoria do cliente - com base na tabela category_clients
      """
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    password = db.Column(db.String(100),nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category_clients.id'), nullable=False)
    vehicles = db.relationship('Vehicle', backref='category_id', lazy=True)
    rent = db.relationship('Rent', backref='id', lazy=True)

class Type(db.Model):
    """
         Criação da tabela Type para cadastro dos tipos de veiculos

         id do cliente
         tipo do veiculo

         """
    __tablename__ = "type_vehicle"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50),nullable=False, unique=True)
    vehicles = db.relationship('Vehicle', backref='id', lazy=True)

class Vehicle(db.Model):
    """
          Criação da tabela Vehicle para cadastro dos veiculos

          id do veiculo
          id_type com base no tipo de veiculo
          cor do veiculo
          quantidade de lugares no veiculo
          iva - verificar se IVA foi pago
          """
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    id_type = db.Column(db.String(50),db.ForeignKey("type_vehicle.id"),nullable=False)
    color = db.Column(db.String(100),nullable=False)
    place = db.Column(db.Integer,nullable=False)
    service = db.Column(db.Integer, nullable=False)
    iva = db.Column(db.Boolean, nullable=False)
    category = db.Column(db.Integer,db.ForeignKey("clients.category_id"), nullable=False)
    rent = db.relationship('Rent', backref='id', lazy=True)

class Rent(db.Model):

    __tablename__ = "rent"

    id_rent = db.Column(db.Integer,primary_key=True)
    id_client = db.Column(db.Integer,db.ForeignKey("clients.id"), nullable=False)
    id_vehicle = db.column(db.Integer,db.ForeignKey("vehicles.id"))
    pick_up_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    price_day = db.Column(db.Float,nullable=False)
    status_rent = db.Column(db.Boolean,nullable=False)
    total_price = db.Column(db.Float,nullable=False)

with app.app_context():
    db.create_all()
    db.session.commit()


