from flask import Blueprint
import smtplib
from .extensions import db
from .settings import SECRET_KEY,USER_NAME,PASSWORD_EMAIL
from functools import wraps
import jwt
from flask import Blueprint,request,jsonify,Response,session
import random

from .models import User,Role,Service,Observation,code_passwords


auth=Blueprint('auth',__name__)


@auth.route('/login',methods=['POST'])
def login_user():
    try:
        id=request.get_json()['id']
        password=request.get_json()['password']
        try:
            user=User.query.filter_by(identification=id).first()

            if user.check_password(password):
                token_data={
                    "user_id":user.id,
                    "rol_id":user.id_rol
                }
                if user.enable:
                    if user.id_rol == 3 and user.count_login == 0:
                        return jsonify({"Message": "To log in you must change your password"})
                    else:
                        token=jwt.encode(token_data,SECRET_KEY)
                        user.count_login=user.count_login+1
                        db.session.commit()
                        return jsonify({"token":token.decode('UTF-8')})
                else:
                    return jsonify({"message":"you must confirm your account"})
            else:
                return jsonify({"message":"invalid credentials"})
        except:
            return jsonify({"message":"Error invalid request"})
    except:
        return jsonify({"message":"Request invalid"})

@auth.route('/user/confirm/<id>')
def confirm_account(id):
    user = User.query.filter_by(id=id).first()
    try:
        if user.enable:
            return jsonify({"message":"Your account is already confirmed"})
        else:
            user.enable=True
            db.session.commit()
            return jsonify({"message": "Your account has been confirmed"})

    except:
        return jsonify({"message":"Your account could not be confirmed"})



@auth.route('/register/doctor',methods=['POST'])
def add_doctor():
    try:
        token=None
        id = request.get_json()['id']
        email = request.get_json()['email']
        cellphone = request.get_json()['cellphone']
        password = request.get_json()['password']
        name = request.get_json()['name']
        address = request.get_json()['address']
        date = request.get_json()['date']
        rol = request.get_json()['id_rol']

        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        else:
            return jsonify({"message":"a valid token is missing"})
        try:
            data=jwt.decode(token,SECRET_KEY)
            if data['rol_id']==1:
                if id and email and cellphone and password and name and address and date and rol :
                    if rol==3:
                        doctor_new=User(identification=id,email=email,cellphone=cellphone,name=name,address=address,birthdate=date,
                                   id_rol=rol,hospital=data['user_id'],count_login=0)
                        doctor_new.set_password(password)
                        db.session.add(doctor_new)
                        db.session.commit()
                        return jsonify({"id_new":doctor_new.id,"message":"Successful registration"})
                    else:
                        return jsonify({"message":"Rol invalid"})

            else:
                return jsonify({"message":"Error, you are not authorized"})

        except:
            return jsonify({"message":"Invalid"}),400
    except:
        return jsonify({"message":"Error, request invalid"})

@auth.route('/observation',methods=['POST'])
def add_observation():
    try:
        id_patiente=request.get_json()['id_patient']
        state=request.get_json()['state']
        comment=request.get_json()['comment']
        service=request.get_json()['service']
        if 'x-access-token' in request.headers:
            token=request.headers['x-access-token']
        else:
            return jsonify({"message":"a valid token is missing"})
        try:
            data = jwt.decode(token, SECRET_KEY)
            if data['rol_id'] == 3:
                user = User.query.filter_by(identification=id_patiente).first()
                user_doc = User.query.filter_by(id=data['user_id']).first()
                if user.id_rol == 2:
                    service_search = Service.query.filter_by(id=service, id_user=user_doc.hospital).first()
                    if service_search:
                        observation = Observation(id_patient=id_patiente, id_doctor=data['user_id'], patient_state=state,
                                                  comment=comment, service=service)
                        db.session.add(observation)
                        db.session.commit()
                        return jsonify({'message':"The observation has been added"})
                    else:
                        return jsonify({'message': 'the data entered does not match'})
                else:
                    return jsonify({"message": "the patient is not registered"})

            else:
                return jsonify({"message": "Error, you are not authorized"})
        except Exception as err:
            print(err)
            return jsonify({"message":"Error"})
    except:
        return jsonify({"message":"Request invalid"})

@auth.route('/doctors/observation/<id>',methods=['GET'])
def get_doc_observations(id):
    if 'x-access-token' in request.headers:
        token=request.headers['x-access-token']
    else:
        return jsonify({"message":"a valid token is missing"})
    try:
        data = jwt.decode(token, SECRET_KEY)
        if data['rol_id'] == 3:
            search=db.session.query(Observation,User,Service).filter(Observation.id_doctor==id).filter(Observation.service==Service.id).filter(Observation.id_patient==User.identification).all()
            print(search)
            list_search=[]
            for obj in search:
                find={
                    'id_observation':obj[0].id,
                    'id_doctor':obj[0].id_doctor,
                    'id_patient':obj[0].id,
                    'name_patient':obj[1].name,
                    'comment':obj[0].comment,
                    'identification':obj[1].identification,
                    'service_name':obj[2].name
                }
                list_search.append(find)
            return jsonify(list_search)
        else:
            raise
    except:
        return jsonify({"message":"Invalid rol"})


@auth.route('/hospital/observation/<id>',methods=['GET'])
def get_hos_observations(id):
    if 'x-access-token' in request.headers:
        token=request.headers['x-access-token']
    else:
        return jsonify({"message":"a valid token is missing"})
    try:
        data = jwt.decode(token, SECRET_KEY)
        if data['rol_id'] == 1:
            search=db.session.query(Observation,User,Service).filter(Observation.id_doctor==User.id,User.hospital==id,Observation.service==Service.id).all()

            list_search = []
            for obj in search:
                find = {
                    'id_observation': obj[0].id,
                    'id_doctor': obj[0].id_doctor,
                    'id_patient': obj[0].id_patient,
                    'name_doctor': obj[1].name,
                    'comment': obj[0].comment,
                    'identification': obj[1].identification,
                    'service_name': obj[2].name
                }
                list_search.append(find)
            return jsonify(list_search)
        else:
            raise
    except:
        return jsonify({"message":"Invalid rol"})

@auth.route('/patient/observation/<id>',methods=['GET'])
def get_pat_observations(id):
    if 'x-access-token' in request.headers:
        token=request.headers['x-access-token']
    else:
        return jsonify({"message":"a valid token is missing"})
    try:
        data = jwt.decode(token, SECRET_KEY)
        if data['rol_id'] == 2:
            search=db.session.query(Observation,User,Service).filter(Observation.id_patient==id,Observation.id_doctor==User.id,Observation.service==Service.id).all()

            list_search = []
            for obj in search:
                find = {
                        'id_observation': obj[0].id,
                        'id_doctor': obj[0].id_doctor,
                        'id_patient': obj[0].id_patient,
                        'name_doctor': obj[1].name,
                        'comment': obj[0].comment,
                        'identification': obj[1].identification,
                        'service_name': obj[2].name,
                        'state':obj[0].patient_state
                }
                list_search.append(find)
            return jsonify(list_search)
        else:
            raise
    except:
        return jsonify({"message":"invalid role"})

@auth.route('/user/restore/<id>',methods=['GET'])
def send_code(id):
    try:
        user=User.query.filter_by(identification=str(id)).first()
        print(user.id)
        if user:
            user_restore=code_passwords.query.filter_by(id_user=user.id).first()
            if user_restore:
                if user_restore and user_restore.use=="No":
                    send_email(user.email,user_restore.code)
                    return jsonify({'code': user_restore.code})
                else :
                    user_restore.code=generate_code()
                    send_email(user.email, user_restore.code)
                    user_restore.use="No"
                    db.session.commit()
                    return jsonify({'code':user_restore.code})
            else:
                code_generate=generate_code()
                code=code_passwords(id_user=user.id,code=code_generate,use="No")
                db.session.add(code)
                send_email(user.email, code_generate)
                db.session.commit()
                return jsonify({'code':code_generate})
        else:
            return jsonify({'message': 'user not found'}), 404
    except Exception as err:
        print(err)
        return jsonify({'message':'error'})

@auth.route('/user/restore/<id>',methods=['POST'])
def restor_password(id):
    new_pass=request.get_json()['password']
    code_send=request.get_json()['code']
    try:
        user = User.query.filter_by(identification=id).first()
        code=code_passwords.query.filter_by(id_user=user.id).first()
        print(type(code_send))
        print(type(id))
        print(user.id,(type(code.code)))
        if  str(code.code)==str(code_send) and str(user.identification)==str(id) and code.use!="Si":
            user.set_password(new_pass)
            code.use="Si"
            db.session.commit()
            return jsonify({"message":"The password has been updated"})
        else:
            return jsonify({"message":"The password hasn't been updated"})
    except:
        return jsonify({"message":"The password hasn't been updated"})


def generate_code():
    code=""
    for i in range(1,7):
        code+=str(random.randrange(10))
    return code

def send_email(email,code):
    from_address=USER_NAME
    to=email
    subject="FlaskHealth restor your password"
    message="Your restoration code is: \n" \
            +str(code)
    message = 'Subject:{}\n\n{}'.format(subject, message)
    server = smtplib.SMTP('smtp.gmail.com:587')
    server.starttls()
    server.login(USER_NAME, PASSWORD_EMAIL)
    server.sendmail(from_address, to, message)
    server.quit()