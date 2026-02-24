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




















