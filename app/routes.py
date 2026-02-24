from flask import request,jsonify,g
from app.auth import generate_access_token,generate_refresh_token,login_required,verify_token
def register_routes(app):
    service = app.config["service"]

    @app.route("/")
    def home():
        return {"message :":"Banking API is running."}
    
    @app.route("/accounts", methods=["POST"])
    def create_account():
        data = request.get_json(silent=True) or {}
        print("Incoming data..",data)
        name = data.get("name")
        pin = data.get("pin")
        initial_deposit = data.get("initial_deposit")
        account_number = service.create_account(name,pin,initial_deposit)
        return {"message":"Account created successfully!",
                "account_number" : account_number},201
    
    @app.route("/accounts/<int:account_number>",methods=["GET"])
    @login_required
    def get_balance(account_number):
        if g.account_number != account_number:
            return {"error":"Unauthorize access"},401
        balance = service.view_balance(account_number)
        return{"account_number":account_number,
            "balance":balance},200
    
    @app.route("/accounts/<int:account_number>/deposit",methods=["POST"])
    @login_required
    def deposit(account_number):
        data = request.get_json(silent=True) or {}
        amount = float(data.get("amount"))
        if g.account_number != account_number:
            return {"error":"Unauthorize access"},401
        if amount is None:
            return {"error":"Amount is required"},400
        new_balance = service.deposit(account_number,amount)
        return {"account_number":account_number,
                "new_balance":new_balance,
                "message":"Deposit successful"},200
    
    @app.route("/accounts/<int:account_number>/withdraw",methods=["POST"])
    @login_required
    def withdraw(account_number):
        data = request.get_json(silent=True) or {}
        amount = float(data.get("amount"))
        if g.account_number != account_number:
            return {"error":"Unauthorize access"},401
        if amount is None:
            return {"error":"Amount is required"},400
        new_balance = service.withdraw(account_number,amount)
        return {"account_number":account_number,
                "new_balance":new_balance,
                "message":"Withdraw successful"},200
    
    @app.route("/accounts/<int:account_number>/transactions",methods=["GET"])
    @login_required
    def get_transactions(account_number):
        if g.account_number != account_number:
            return {"error":"Unauthorize access"},401
        transactions = service.view_transactions(account_number)
        result = []
        for txn in transactions:
            result.append({
                "transaction_type":txn.transaction_type,
                "amount":txn.amount,
                "balance_after":txn.balance_after,
                "timestamp":txn.timestamp
            })
        return {"account_number":account_number,
                "transactions":result},200
    
    @app.route("/accounts/<int:account_number>/unlock",methods=["POST"])
    def unlock_account(account_number):
        data = request.get_json(silent=True) or {}
        provided_key = str(data.get("admin_key"))
        account_status = service.unlock_account(account_number,provided_key)
        return {"account_number":account_number,"message":account_status}
    
    @app.route("/auth/login/",methods=["POST"])
    def login():
        data = request.get_json(silent=True) or {}
        account_number = data.get("account_number")
        pin = data.get("pin")
        try :
            service.authenticate(account_number,pin)
            access_token = generate_access_token(account_number)
            refresh_token = generate_refresh_token(account_number)
            return {"message":"login successful","access_token":access_token,"refresh_token":refresh_token},200
        except Exception as e:
            return {"error":str(e)},401
        
    @app.route("/auth/refresh",methods=["POST"])
    def refresh():
        auth_header = request.headers.get("Authorization")

        if not auth_header :
            return {"error":"Authorization header is missing."},401
        
        parts = auth_header.split(" ")

        if len(parts)!=2 or parts[0] != "Bearer":
            return {"error":"Invalid Authorization header format"},401
        
        token =  parts[1]
        try :
            payload = verify_token(token)

            if payload.get("type") != "refresh":
                return {"error":"Invalid refresh token"},401
            
            new_access_token = generate_access_token(payload["sub"])
            return {"access_token":new_access_token},200
        except Exception as e:
            return {"error":str(e)},401