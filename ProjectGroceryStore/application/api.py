from flask import Flask, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from werkzeug.exceptions import HTTPException
import json
from application.models import User,Section ,Products,Order
from application.database import db

class NotFoundError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class InternalServerError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class ExistsError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class NotExistsError(HTTPException):
    def __init__(self, status_code):
        self.response = make_response('', status_code)

class BuisnessValidationError(HTTPException):
    def __init__(self, status_code, error_code, error_message):
        message={"error_code": error_code, "error_message": error_message}
        self.response = make_response(json.dumps(message), status_code)




User_parser = reqparse.RequestParser()
User_parser.add_argument("full_name")
User_parser.add_argument("user_name")
User_parser.add_argument("Email")
User_parser.add_argument("password")
User_parser.add_argument("Role")
user_output={
    "id":fields.Integer,
    "full_name":fields.String,
    "user_name":fields.String,
    "Email":fields.String,
    "password":fields.String,
    "Role":fields.String
}
class UserApi(Resource):
    @marshal_with(user_output)
    def get(self,id):
        try:
            print(id)
            user=db.session.query(User).filter(User.id==id).first()
            if  user:
                return user
            else:
                raise NotFoundError(status_code=404)
        
        except NotFoundError as nfe:
                raise nfe
        except Exception as e:
            raise InternalServerError(status_code=500)

    @marshal_with(user_output) 
    def put(self,id):
        args = User_parser.parse_args()
        full_name=args.get("full_name",None)
        user_name=args.get("user_name",None)
        email=args.get("Email",None)
        password=args.get("password",None)
        Role=args.get("Role",None)

        if full_name is None:
            raise BuisnessValidationError(status_code=400, error_code="User1001", error_message="full name is required")
        if user_name is None:
            raise BuisnessValidationError(status_code=400, error_code="User1002", error_message="User name is required")
        if email is None:
            raise BuisnessValidationError(status_code=400,error_code="User1003",error_message="Email id is required")
        if password is None:
            raise BuisnessValidationError(status_code=400, error_code="User1004", error_message="password is required")
        if Role is None:
            raise BuisnessValidationError(status_code=400, error_code="User1005", error_message="Role is required")
        if Role !="Admin" and Role != "user":
            raise BuisnessValidationError(status_code=400,error_code="User1006",error_message="Role could be either Admin or user")
        
        user=User.query.filter(User.id==id).first()
        if user:
            user.full_name=full_name
            user.user_name=user_name
            user.Email=email
            user.password=password
            user.Role=Role
            db.session.commit()
            return user,200
        raise NotFoundError(status_code=404)
    
    def delete(self,id):
        user=User.query.filter(User.id==id).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            return "",200
        raise NotFoundError(status_code=404)
    
    def post(self):
        args = User_parser.parse_args()
        full_name=args.get("full_name",None)
        user_name=args.get("user_name",None)
        email=args.get("Email",None)
        password=args.get("password",None)
        Role=args.get("Role",None)

        if full_name is None:
            raise BuisnessValidationError(status_code=400, error_code="User1001", error_message="full name is required")
        if user_name is None:
            raise BuisnessValidationError(status_code=400, error_code="User1002", error_message="User name is required")
        if email is None:
            raise BuisnessValidationError(status_code=400,error_code="User1003",error_message="Email id is required")
        if password is None:
            raise BuisnessValidationError(status_code=400, error_code="User1004", error_message="password is required")
        if Role is None:
            raise BuisnessValidationError(status_code=400, error_code="User1005", error_message="Role is required")
        if Role !="Admin" and Role != "user":
            raise BuisnessValidationError(status_code=400,error_code="User1006",error_message="Role could be either Admin or user")
            
        user=db.session.query(User).filter((User.user_name == user_name) | (User.Email == email)).first()
        if user:
            print("HEllo we are in to check duplicate data")
            raise BuisnessValidationError(status_code=400, error_code="User1007", error_message="Duplicate user")             
            
        new_user=User(full_name=full_name,user_name=user_name,Email=email,password=password,Role=Role)
        db.session.add(new_user)
        db.session.commit()
        return "",201
    








        
