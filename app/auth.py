import jwt
from app.config import Config
from functools import wraps
from flask import request,g
from datetime import datetime,timezone,timedelta
from exceptions.token_expired_exception import TokenExpiredException
from exceptions.invalid_token_exception import InvalidTokenException
from exceptions.unauthorized_exception import Unauthorized

#! application context coupling:↓
# from flask import current_app

#generate_access_token
def generate_access_token(account_number):
    
    payload={#!  "sub":account_number,--> error(The "sub" (subject) claim MUST be a string.)
            "sub":str(account_number),#subject
            "type":"access",
            "role":"user",#role_ready
            "iat":datetime.now(timezone.utc),#issued_at
            "exp":datetime.now(timezone.utc)+timedelta(minutes=15)#expires_at
             }
    
    return jwt.encode(payload,Config.SECRET_KEY,algorithm="HS256")

#generate_refresh_token
def generate_refresh_token(account_number):

    payload={#!  "sub":account_number,--> error(The "sub" (subject) claim MUST be a string.)
            "sub":str(account_number),
            "type":"refresh",
            "role":"user",
            "iat":datetime.now(timezone.utc),
            "exp":datetime.now(timezone.utc)+timedelta(days=7)
            }
    
    return jwt.encode(payload,Config.SECRET_KEY,algorithm="HS256")

#verify token
def verify_token(token):
    try:
        # print("secret_key",Config.SECRET_KEY)
        # print("token",token)
        payload = jwt.decode(token,Config.SECRET_KEY,algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise TokenExpiredException("Token has expired.")
    except jwt.InvalidTokenError:
        raise InvalidTokenException("Invalid authentication token.")

#decorator
def login_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        auth_header = request.headers.get("Authorization")
       
        
        if not auth_header:
            raise Unauthorized("Authorization header is missing.")
        
        try:
            parts = auth_header.split(" ")
            #!because i am using postman for api testing : header is "Bearer Token" or else in "Bearer" it will return error
            if len(parts)!=2 or parts[0] != "Bearer":
                raise Unauthorized("Invalid Authorization header format.")
            
            token =  parts[1]
            payload = verify_token(token)
            if payload.get("type")!="access":
                return {"error":"Access token reuired"},401
            g.account_number = int(payload["sub"]) #! payload must return int value..
        except TokenExpiredException as e:
            return {"error": str(e)}, 401
        except InvalidTokenException as e:
            return {"error": str(e)}, 401
        except Unauthorized as e:
            return {"error": str(e)}, 401
        
        return f(*args,**kwargs)
    return decorated