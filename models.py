from app import db,app




class Category(db.Model):
    """
    Criação da tabela category_clients para passar que tipo de categoria o cliente se cadastrou

    categoria : Gold, Silver, Economic
    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    category = db.Column(db.String(50),nullable=False, unique=True)


    def __init__(self,category):
        self.category = category


class User(db.Model):
    """
      Criação da tabela User para cadastro dos clientes

      id do cliente
      nome do cliente
      email do cliente
      senha do cliente
      categoria do cliente - com base na tabela categories
      """
    __tablename__ = "clients"

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    name = db.Column(db.String(50),nullable=False)
    email = db.Column(db.String(100),nullable=False, unique=True)
    password = db.Column(db.String(500),nullable=False)
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)



    def __int__(self,name,email,password,categories_id):
        self.name = name
        self.email = email
        self.password = password
        self.categories_id = categories_id





class Type(db.Model):
    """
         Criação da tabela Type para cadastro dos tipos de veiculos
            tipo: Carro, moto
         id do cliente
         tipo do veiculo

         """
    __tablename__ = "vehicle_types"

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    type = db.Column(db.String(50),nullable=False, unique=True)




    def __int__(self, type):
        self.type = type


    def __repr__(self):
        return f' {self.type}'

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

    id = db.Column(db.Integer, primary_key=True,nullable=False)
    type_id = db.Column(db.Integer,db.ForeignKey("vehicle_types.id"),nullable=False)
    name = db.Column(db.String(100),nullable=False)
    status = db.Column(db.Boolean,nullable=False)
    service = db.Column(db.Integer, nullable=False)
    iva = db.Column(db.Boolean, nullable=False)
    price_day = db.Column(db.Integer,nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey("categories.id"), nullable=False)



    def call_price(self):
        return self.price_day

class Rent(db.Model):

    __tablename__ = "rents"

    id = db.Column(db.Integer,primary_key=True,nullable=False)
    client_id = db.Column(db.Integer,db.ForeignKey("clients.id"), nullable=False)
    vehicle_id = db.Column(db.Integer,db.ForeignKey("vehicles.id"), nullable=False)
    pick_up_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    price_day = db.Column(db.Float,nullable=False)
    status_rent = db.Column(db.Boolean,nullable=False)
    total_price = db.Column(db.Float,nullable=False)



with app.app_context():



    db.create_all()
    db.session.commit()
