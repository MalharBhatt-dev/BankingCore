import os
import sqlite3
from datetime import datetime,timedelta
class ServiceRequestRepository:
    def __init__(self):

        #!PATH HANDLING↓import os
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        DB_PATH = os.path.join(BASE_DIR, "database", "accounts.db")

        self.conn = sqlite3.connect(DB_PATH,check_same_thread=False)
        self.conn.execute("PRAGMA foreign_key = ON")
    
    def create_request(self,account_number,query_type,description):
        created_at = datetime.now().strftime("%D-%M-%Y %H:%M:%S")
        status = "PENDING"

        c= self.conn.cursor()
        c.execute("""insert into service_requests (account_number , query_type,description,created_at) values (?, ?, ?, ?)""",(account_number,query_type,description,created_at))
        
        #!remove it after the addition of the features in the service layer.
        self.conn.commit()

a = ServiceRequestRepository()
a.create_request(1001,"pin_change","PIN CHANGED")