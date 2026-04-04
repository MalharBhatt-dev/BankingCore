from flask import request,jsonify,g,render_template
from app.extensions import limiter
from repository.account_repository import AccountRepository
from repository.service_request_repository import ServiceRequestRepository
from services.banking_services import BankingServices
from services.service_request_service import ServiceRequestService
from app.auth import generate_access_token,generate_refresh_token,login_required,role_required,verify_token
def register_routes(app):
    service = app.config["service"]
    request_service = app.config["request_service"]
    
    # @app.route("/")
    # def home():
    #     return "OK", 200
    
    @app.route("/health")
    def health():
        return "healthy", 200

    @app.route("/accounts", methods=["POST"])
    def create_account():
        data = request.get_json(silent=True) or {}
        print("Incoming data..",data)
        name = data.get("name")
        pin = data.get("pin")
        initial_deposit = float(data.get("initial_deposit"))
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
    def locked_accounts():
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
    
    @app.route("/requests",methods=["POST"])
    @login_required
    # @role_required("employee")
    def create_request():
        data = request.get_json(silent=True) or {}

        employee_id = data.get("employee_id","1004")
        query_type = data.get("query_type") or data.get("request_type")
        description = data.get("description")

        #validate 
        if not query_type:
            return {"error":"Query type required"},400
        
        if not description:
            return {"error":"Description required"},400
        
        request_service.create_request(g.account_number,employee_id,query_type,description)

        return {"message":"Request created successsfully"},201

    @app.route("/requests/user",methods=["GET"])
    @login_required
    @role_required("admin")
    def user_requests():
        requests = request_service.get_requests_logs()
        return {"requests":requests}

    @app.route("/requests/my",methods=["GET"])
    @login_required
    def my_requests():
        requests = request_service.get_user_requests(g.account_number)
        return {"requests":requests}

    @app.route("/employee/requests",methods=["GET"])
    @login_required
    @role_required("employee")
    def pending_requests():
        requests = request_service.get_pending_requests(g.account_number)
        return {"requests":requests}

    @app.route("/employee/requests/<int:request_id>/approve",methods=["POST"])
    @login_required
    @role_required("employee")
    def approve_request(request_id):
        request_service.approve_request(request_id,g.account_number)
        return {"message":"Request approved"}
    
    @app.route("/employee/requests/<int:request_id>/reject",methods=["POST"])
    @login_required
    @role_required("employee")
    def reject_request(request_id):
        request_service.reject_request(request_id,g.account_number)
        return {"message":"Request rejected"}
    
    @app.route("/requests/<int:request_id>/submit",methods=["POST"])
    @login_required
    def submit_request(request_id):
        data = request.get_json(silent=True) or {}
        request_service.submit_request(request_id,g.account_number,data)
        return {"message":"Request submitted successfully"}
    
    @app.route("/requests/<int:request_id>/complete",methods=["GET"])
    @login_required
    def complete_request(request_id):
        request_service.complete_request(request_id)
        return {"message":"Request completed successfully"}

    @app.route("/update/account_holder_name",methods=["POST"])
    @login_required
    def update_account_holder_name():
        data = request.get_json(silent=True) or {}
        account_holder_name = data.get("new_name")
        service.update_account_holder_name(g.account_number,account_holder_name)
        return {"message":"Account Holder Name updated successfully"}
    
    @app.route("/update/pin_number",methods=["POST"])
    @login_required
    def update_pin_number():
        data=request.get_json(silent = True) or {}
        pin_number = data.get("new_pin")
        service.update_pin_number(g.account_number,pin_number)
        return{"message":"PIN number updated successfully"}
    
    #NOTE : #h Future Request Feature Implementation :
    # @app.route("/update/contact",methods=["POST"])
    # @login_required
    # def update_contact():
    #     data = request.get_json(silent =True) or {}
    #     contact_number = data.get("phone")
    #     email = data.get("email")
    #     return{"message":"This feature is under development"}
    
    # @app.route("/update/kyc",methods=["POST"])
    # @login_required
    # def update_kyc():
    #     data = request.get_json(silent= True) or {}
    #     address = data.get("address")
    #     id_number = data.get("id_number")
    #     service.update_kyc()
    #     return{"message":"This feature is under development"}
    
    # @app.route("/update/account_close",methods=["POST"])
    # @login_required
    # def account_close():
    #     data = request.get_json(silent = True) or {}
    #     service.account_close(g.account_number)
    #     return{"message":"Account is closed successdfully"}
    
    

    @app.route("/")
    def home():
        try:
            return render_template("/index.html")
        except Exception as e:
            return f"ERROR: {str(e)}", 500

    @app.route("/pages/<path:path>")
    def serve_page(path):
        try:
            return render_template(path)
        except Exception as e:
            return str(e), 500

    # def get_service(app):
    #     if not app.config["service"]:
    #         repo = AccountRepository()
    #         app.config["service"] = BankingServices(
    #             repo,app.config["ADMIN_KEY"],app.logger
    #         )
    #     return app.config["service"]
    
    # service = get_service(app)