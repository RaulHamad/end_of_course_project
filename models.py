from app import db,app




class Category(db.Model):
    """
    Criação da tabela categories para passar que tipo de categoria que o cliente se cadastrou

    category : Gold, Silver, Economic
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
         id :do cliente
         type: do veiculo

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

          id: id do veiculo
          type_id: type com base na tabela vehicle_types
          name:  nome do veiculo
          status: se irá ficar disponivel para locação ou não
          service: integer que ao atingir 5 locações, irá para revisão(30 dias indisponiveis para locação)
          iva: verificar se IVA foi pago
          price_day: preço do aluguel diário do veículo
          category_id: categoria com base em category_id
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
    """
    Tabela para cadastrar locações de veículos

    client_id: id do cliente cadastrado
    vehicle_id: id do veículo cadastrado
    pick_up_date: data para retirada do veículo
    return_date: data para devolução do veículo
    price_day: preço do aluguel diário do veículo
    total_price: preço total a ser pago
    """

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
