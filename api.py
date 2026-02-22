from flask import Flask,request
from dotenv import load_dotenv
from repository.account_repository import AccountRepository
from services.banking_services import BankingServices
from exceptions.base_exception import BankingException
import os
app = Flask(__name__)

repo = AccountRepository()
service = BankingServices(repo)

load_dotenv()

ADMIN_KEY = os.getenv("ADMIN_KEY")

@app.route("/")
def home():
    return {"message :":"Banking API is running."}

@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    print("Incoming data..",data)
    name = data.get("name")
    pin = data.get("pin")
    initial_deposit = data.get("initial_deposit")
    account_number = service.create_account(name,pin,initial_deposit)
    return {"message":"Account created successfully!",
            "account_number" : account_number},201

@app.route("/accounts/<int:account_number>",methods=["POST"])
def get_balance(account_number):
    data = request.get_json()
    pin = str(data.get("pin"))
    balance = service.view_balance(account_number,pin)
    return{"account_number":account_number,
           "balance":balance},200

@app.route("/accounts/<int:account_number>/deposit",methods=["POST"])
def deposit(account_number):
    data = request.get_json()
    pin = str(data.get("pin"))
    amount = float(data.get("amount"))
    new_balance = service.deposit(account_number,pin,amount)
    return {"account_number":account_number,
            "new_balance":new_balance,
            "message":"Deposit successful"},200


@app.route("/accounts/<int:account_number>/withdraw",methods=["POST"])
def withdraw(account_number):
    data = request.get_json()
    pin = str(data.get("pin"))
    amount = float(data.get("amount"))
    new_balance = service.withdraw(account_number,pin,amount)
    return {"account_number":account_number,
            "new_balance":new_balance,
            "message":"Withdraw successful"},200


@app.route("/accounts/<int:account_number>/transactions",methods=["POST"])
def get_transactions(account_number):
    data = request.get_json()
    pin = str(data.get("pin"))
    transactions = service.view_transactions(account_number,pin)
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
    data = request.get_json()
    provided_key = str(data.get("admin_key"))
    account_status = service.unlock_account(account_number,provided_key)
    return {"account_number":account_number,"message":account_status}

@app.errorhandler(BankingException)
def handle_banking_exceptions(error):
    return{"error":str(error)},400

@app.errorhandler(Exception)
def handle_system_exceptions(error):
    print("system error",error)
    return{"error":"internal server error"},500

if __name__ == "__main__":
    app.run(debug=True)
