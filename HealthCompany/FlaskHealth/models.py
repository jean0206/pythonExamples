from .extensions import db

from flask_login import UserMixin

from werkzeug.security import generate_password_hash,check_password_hash

class User(UserMixin,db.Model):
    __tablename__='users'
    __table_args__ = {'extend_existing': True}
    id=db.Column(db.Integer,primary_key=True)
    identification=db.Column(db.String,unique=True)
    email=db.Column(db.String(50),unique=True)
    cellphone=db.Column(db.String(15))
    password_hash=db.Column('password',db.String(100))
    name=db.Column(db.String(100))
    address=db.Column(db.String(100))
    enable=db.Column(db.Boolean,default=False,nullable=True)
    hospital=db.Column(db.Integer,nullable=True)
    count_login=db.Column(db.Integer)
    birthdate=db.Column(db.Date,nullable=True)
    id_rol=db.Column(db.Integer,db.ForeignKey('role.id'))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Role(db.Model):
    __tablename__='role'
    __table_args__ = {'extend_existing': True}
    id=db.Column(db.Integer,primary_key=True)
    rol_name=db.Column(db.String(100))

class Observation(db.Model):
    __tablename__='observation'
    __table_args__ = {'extend_existing': True}
    id=db.Column(db.Integer,primary_key=True)
    id_patient = db.Column(db.String, db.ForeignKey('users.identification'))
    id_doctor=db.Column(db.Integer, db.ForeignKey('users.id'))
    patient_state=db.Column(db.String())
    comment=db.Column(db.String())
    service=db.Column(db.Integer,db.ForeignKey('services.id'))


class Service(db.Model):
    __tablename__='services'
    id=db.Column(db.Integer,primary_key=True)
    id_user=db.Column(db.Integer)
    name=db.Column(db.String(100))

class code_passwords(db.Model):
    __tablename__='code_passwords'
    id=db.Column(db.Integer,primary_key=True)
    id_user=db.Column(db.Integer,unique=True)
    code=db.Column(db.String)
    use=db.Column(db.String)