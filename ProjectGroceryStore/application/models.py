from .database import db

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    full_name=db.Column(db.String,nullable=False)
    user_name=db.Column(db.String,nullable=False,unique=True)
    Email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    Role=db.Column(db.String,nullable=False)

class Section(db.Model):
    __tablename__ ='section'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    admin_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)

class Products(db.Model):
    __tablename__ = 'products'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    name=db.Column(db.String,nullable=False)
    manufacture_date=db.Column(db.String,nullable=False)
    expiry_date=db.Column(db.String,nullable=False)
    rate=db.Column(db.Integer,nullable=False)
    section_id=db.Column(db.Integer,db.ForeignKey("section.id"),nullable=False)
    admin_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    description=db.Column(db.String,nullable=False)
    Unit=db.Column(db.String, nullable=False)
    Quantity=db.Column(db.Integer,nullable=False)
    

class Order(db.Model):
    __tablename__='order'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    admin_id=db.Column(db.Integer,db.ForeignKey("user.id"),nullable=False)
    user_id=db.Column(db.Integer,nullable=False)
    product_id=db.Column(db.Integer,db.ForeignKey("products.id"),nullable=False)
    rate=db.Column(db.Integer,nullable=False)
    Quantity=db.Column(db.Integer,nullable=False)
    Price=db.Column(db.Integer,nullable=False)
    isActive=db.Column(db.String,nullable=False)
    Date=db.Column(db.String,nullable=True)
    transaction_id=db.Column(db.String,nullable=True)


