from flask import request,jsonify,g
from app.extensions import limiter
from app.auth import generate_access_token,generate_refresh_token,login_required,role_required,verify_token
def register_routes(app):
    service = app.config["service"]

    @app.route("/")
    def home():
        return {"message":"Banking API is running."}
    
    @app.route("/accounts", methods=["POST"])
    def create_account():
        data = request.get_json(silent=True) or {}
        print("Incoming data..",data)
        name = data.get("name")
        pin = data.get("pin")
        account_type = data.get("account_type")
        initial_deposit = float(data.get("initial_deposit"))
        account_number = service.create_account(name,pin,initial_deposit,account_type)
        return {"message":"Account created successfully!",
                "account_number" : account_number},201
    @app.route("/accounts/<int:account_number>/account_type",methods=["GET"])
    @login_required
    def get_account_type(account_number):
        if g.account_number != account_number:
            return {"error":"Unauthorize access"},401
        account_type = service.get_account_type(account_number)
        return{"account_type":account_type,"account_number":account_number}

    @app.route("/accounts/<int:account_number>",methods=["GET"])
    @login_required
    def get_balance(account_number):
        if g.account_number != account_number:
            return {"error":"Unauthorize access"},401
        balance = service.view_balance(account_number)
        return{"account_number":account_number,
            "balance":balance},200
    
    @app.route("/accounts/<int:account_number>/deposit",methods=["POST"])
    @limiter.limit("20 per minute")
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
    @limiter.limit("20 per minute")
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
    
    @app.route("/accounts/<int:from_account>/transfer",methods=["POST"])
    @limiter.limit("5 per minute")
    @login_required
    def transfer_money(from_account):
        data=request.get_json()

        to_account = data.get("to_account")
        amount = float(data.get("amount"))

        result = service.transfer(from_account,to_account,amount)

        return {
            "message":"Transfer successful",
            "from_account":from_account,
            "to_account":to_account,
            "amount":amount
        },200

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

    @app.route("/admin/unlock",methods=["POST"])
    @login_required
    @role_required("admin")
    def admin_unlock():
        data = request.get_json(silent=True) or {}
        account_number = data.get("account_number")
        admin_key = str(data.get("admin_key"))
        account_status = service.unlock_account(account_number,admin_key)
        return {"message":account_status,"account_number":account_number},200
    
    @app.route("/admin/stats",methods=["GET"])
    @login_required
    @role_required("admin")
    def admin_stats():
        last_event = service.get_last_lock_event()
        return {"total_balance":service.get_total_balance(),
                "locked_accounts":service.get_locked_accounts_count(),
                "total_accounts":service.get_total_accounts_count(),
                "last_locked_account":last_event}
    
    @app.route("/admin/events",methods=["GET"])
    @login_required
    @role_required("admin")
    def get_security_stats():
        events = service.get_security_events()
        result =[]
        for e in events:
            result.append({
                "account_number":e.account_number,
                "event":e.transaction_type,
                "balance":e.balance_after,
                "timestamp":e.timestamp
            })
        return {"events":result},200
    
    @app.route("/admin/locked-accounts",methods=["GET"])
    @login_required
    @role_required("admin")
    def locke_accounts():
        accounts = service.get_locked_accounts()
        return {"accounts":accounts},200

    @app.route("/auth/login",methods=["POST"])
    @limiter.limit("5 per minute")
    def login():
        data = request.get_json(silent=True) or {}
        account_number = data.get("account_number")
        pin = data.get("pin")
        try :   
            account = service.authenticate(account_number,pin)
            role = account.role
            access_token = generate_access_token(account_number,role)
            refresh_token = generate_refresh_token(account_number,role)
            return {"message":"login successful","access_token":access_token,"refresh_token":refresh_token},200
        except Exception as e:
            return {"error":str(e)},401
    
    @app.route("/auth/refresh",methods=["POST"])
    @limiter.limit("10 per minute")
    def refresh():
        auth_header = request.headers.get("Authorization")

        if not auth_header :
            return {"error":"Authorization header is missing."},401
        
        parts = auth_header.split(" ")

        if len(parts)!=2 or parts[0] != "Bearer":
            return {"error":"Invalid Authorization  header format"},401
        
        token =  parts[1]
        try :
            payload = verify_token(token)

            jti = payload.get("jti")
            if service.is_blacklisted(jti):
                return {"error":"Refresh token revoked."},401
            if payload.get("type") != "refresh":
                return {"error":"Invalid refresh token"},401
            service.black_list_token(jti)

            #generate new token
            new_refresh_token = generate_refresh_token(payload["sub"],payload["role"])
            new_access_token = generate_access_token(payload["sub"],payload["role"])
            
            return {"access_token":new_access_token,"refresh_token":new_refresh_token},200
        except Exception as e:
            return {"error":str(e)},401
        
    @app.route("/auth/logout",methods=["POST"])
    def logout():
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return {"error":"Authorization header missing"},401
        
        parts = auth_header.split(" ")

        if len(parts) != 2 or parts[0] != "Bearer":
            return {"error":"Invalid authorization header format."},401
        
        refresh_token = parts[1]

        try:
            payload = verify_token(refresh_token)

            if payload.get("type") != "refresh":
                return{"error":"refresh token required"},401
            
            jti = payload.get("jti")
            service.black_list_token(jti)
            return {"message":"Logged out successfully."},200
        except Exception as e:
            return {"error":str(e)},401 
    
  