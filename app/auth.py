import jwt
from datetime import datetime,timezone,timedelta
from app.config import Config
from functools import wraps
from flask import request,g

#! application context coupling:↓
# from flask import current_app

#generate_token
def generate_token(account_number):
    payload={"account_number":account_number,"exp":datetime.now(timezone.utc)+timedelta(minutes=30)}
    token = jwt.encode(payload,Config.SECRET_KEY,algorithm="HS256")
    return token

#verify token
def verify_token(token):
    try:
        payload = jwt.decode(token,Config.SECRET_KEY,algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise Exception("token expired")
    except jwt.InvalidTokenError:
        raise Exception("invalid token")

#decorator
def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth_header = request.headers.get("Authorization")
       
        
        if not auth_header:
            return {"error":"Authorization header is missing."},401
        
        try:
            parts = auth_header.split(" ")
            #!because i am using postman for api testing : header is "Bearer Token" or else in "Bearer" it will return error
            if len(parts)!=2 or parts[0] == "Bearer Token":
                return{"error":"Invalid Authorization header format"},401
            
            token =  parts[1]
            payload = verify_token(token)
            g.account_number = payload["account_number"]
        except Exception as e:
            return {"error":str(e)},401
        return f(*args,**kwargs)
    return decorated