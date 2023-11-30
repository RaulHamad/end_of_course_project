from app import db,app




class Category(db.Model):
    """
    Criação da tabela category_clients para passar que tipo de categoria o cliente se cadastrou

    categoria : Gold, Silver, Economic
    """
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True)
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

    clients_id = db.Column(db.Integer, primary_key=True)
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

    type_id = db.Column(db.Integer, primary_key=True)
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

    id = db.Column(db.Integer, primary_key=True)
    vehicles_type_id = db.Column(db.Integer,db.ForeignKey("vehicle_types.type_id"),nullable=False)
    color = db.Column(db.String(100),nullable=False)
    place = db.Column(db.Integer,nullable=False)
    service = db.Column(db.Integer, nullable=False)
    iva = db.Column(db.Boolean, nullable=False)
    price_day = db.Column(db.Integer,nullable=False)
    category_id = db.Column(db.Integer,db.ForeignKey("categories.category"), nullable=False)

    # # vehicles = db.relationship('Vehicle', backref= 'vehicles', lazy=True)
    # vehicle_category = db.relationship('Category', uselist=False, back_populates="vehicles",
    #                                    cascade="all, delete-orphan",
    #                                    single_parent=True)
    # ref_vehicle = db.relationship('Type', uselist=False, back_populates="vehicles",
    #                               cascade="all, delete-orphan",
    #                               single_parent=True)
    #
    # rent = db.relationship('Rebt', uselist=False, back_populates="vehicles", cascade="all, delete-orphan",
    #                        single_parent=True)

class Rent(db.Model):

    __tablename__ = "rents"

    rent_id = db.Column(db.Integer,primary_key=True)
    client_id = db.Column(db.Integer,db.ForeignKey("clients.clients_id"), nullable=False)
    vehicle_id = db.Column(db.Integer,db.ForeignKey("vehicles.id"))
    pick_up_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    price_day = db.Column(db.Float,nullable=False)
    status_rent = db.Column(db.Boolean,nullable=False)
    total_price = db.Column(db.Float,nullable=False)
    #
    # rent_user = db.relationship('User', uselist=False, back_populates="rents", cascade="all, delete-orphan",
    #                        single_parent=True)
    #
    # rent_vehicle = db.relationship('Vehicle', uselist=False, back_populates="rents", cascade="all, delete-orphan",
    #                        single_parent=True)



with app.app_context():



    db.create_all()
    db.session.commit()
