from flask import Blueprint,request,jsonify,Response
from .extensions import db
from .settings import USER_NAME,PASSWORD_EMAIL

from .models import User,Role,Service
import smtplib
import requests

main=Blueprint('main',__name__)


@main.route('/register/hospital',methods=['POST'])
def register_hospital():
    try:
        id=request.get_json()['id']
        email = request.get_json()['email']
        cellphone = request.get_json()['cellphone']
        password = request.get_json()['password']
        name = request.get_json()['name']
        address = request.get_json()['address']
        services = request.get_json()['services']
        rol=request.get_json()['id_rol']
        if id and email and cellphone and password and name and address and services and rol:
            if rol==1:
                user_hospital=User(identification=id,email=email,cellphone=cellphone,name=name,address=address,birthdate=None,
                               id_rol=rol,count_login=0)
                user_hospital.set_password(password)
                db.session.add(user_hospital)
                db.session.commit()
                send_email(user_hospital.id,user_hospital.email)
                for service in services:
                    sevice_new=Service(id_user=user_hospital.id,name=service)
                    db.session.add(sevice_new)
                    db.session.commit()
                return jsonify({"message":"Successful registration","id":user_hospital.id})

            else:
                return jsonify({"message":"The Role is invalid"}),401
    except:
        return jsonify({"message":"The request is invalid"}),401

@main.route('/user/change/<id>',methods=['POST'])
def change_password(id):
    try:
        past_pass=request.get_json()['pass']
        new_pass=request.get_json()['new_pass']
        try:
            user=User.query.filter_by(identification=id).first()
            if user.check_password(past_pass):
                user.set_password(new_pass)
                user.count_login=user.count_login+1
                db.session.commit()
                return jsonify({"message":"The password has been updated"})
            else:
                return jsonify({"message":"invalid credentials"})
        except:
            return jsonify({"Message":"Error"})
    except:
        return jsonify({"message":"The request is invalid"}),401



@main.route('/register/patient',methods=['POST'])
def register_patient():
    try:
        id = request.get_json()['id']
        email = request.get_json()['email']
        cellphone = request.get_json()['cellphone']
        password = request.get_json()['password']
        name = request.get_json()['name']
        address = request.get_json()['address']
        date=request.get_json()['date']
        rol = request.get_json()['id_rol']
        hospital=request.get_json()['hospital']

        if id and email and cellphone and password and name and address and hospital and rol and date:
            try:
                user=User.query.filter_by(id=hospital).first()
                if user:
                    if rol==2:
                        user_new=User(identification=id,email=email,cellphone=cellphone,name=name,address=address,birthdate=date,
                                   id_rol=rol,hospital=hospital,count_login=0)
                        user_new.set_password(password)
                        db.session.add(user_new)
                        db.session.commit()
                        return jsonify({"message":"Successful registration"})
                    else:
                        return jsonify({"message":"Rol invalid"})
                else:
                    return jsonify({"message":"not exists hospital"})
            except Exception as err:
                print(err)
                return jsonify({"message":"Error"}),404
    except:
        return jsonify({"message":"The request is invalid"}),401

def send_email(id,email):
    from_address=USER_NAME
    to=email
    subject="FlaskHealth confirm your account"
    message="Confirm your account by entering the following link: \n" \
            "http://127.0.0.1:5000/user/confirm/"+str(id)
    message = 'Subject:{}\n\n{}'.format(subject, message)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(USER_NAME, PASSWORD_EMAIL)
    server.sendmail(from_address, to, message)
    server.quit()