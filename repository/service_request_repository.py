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
    
    def create_request(self,account_number,employee_id,query_type,description):
        created_at = datetime.now().isoformat()

        c= self.conn.cursor()
        c.execute("""insert into service_requests (account_number, query_type, description, created_at, employee_id) values (?, ?, ?, ?, ?)""",(account_number,query_type,description,created_at,employee_id))
    
    def get_requests_logs(self):
        c = self.conn.cursor()
        c.execute("""select * from request_submissions order by submitted_at""")
        rows = c.fetchall()
        return rows

    def get_user_requests(self,account_number):
        c=self.conn.cursor()
        c.execute("""select * from service_requests where account_number = ? order by created_at desc""",(account_number,))
        rows = c.fetchall()
        return rows
    
    def get_pending_requests(self,account_number):
        c= self.conn.cursor()
        c.execute("""select * from service_requests where (status = 'PENDING' and employee_id = ?) order by created_at ASC""",(account_number,))
        rows = c.fetchall()
        return rows
    
    def get_request(self,request_id):
        c = self.conn.cursor()
        c.execute("""
        SELECT *
        FROM service_requests
        WHERE id = ?""",(request_id,))
        return c.fetchone()
    
    def approve_request(self,request_id,employee_id,expires_at):
        c = self.conn.cursor()
        approved_at = datetime.now().isoformat()
        c.execute("""UPDATE service_requests SET status = ? ,approved_by_employee = ?,approved_at = ?,expires_at =? where id = ?""",("APPROVED",employee_id,approved_at,expires_at,request_id))

    def reject_request(self,request_id,employee_id):
        c = self.conn.cursor()
        c.execute("""UPDATE service_requests SET status = ? , approved_by_employee = ? where id = ?""",("REJECTED",employee_id,request_id))
    
    def submit_request(self,request_id,account_number,submission_data,employee_id):
        c=self.conn.cursor()
        submitted_at = datetime.now().isoformat()
        c.execute("""INSERT INTO request_submissions (request_id,account_number,submission_data,submitted_at) values (?,?,?,?)""",(request_id,account_number,submission_data,submitted_at))
        c.execute("""UPDATE service_requests SET status = ? , approved_by_employee = ? where id = ?""",("SUBMITTED",employee_id,request_id))
    
    def complete_request(self,request_id):
        c = self.conn.cursor()
        c.execute("""update service_requests set status = ? where id = ?""",("COMPLETED",request_id))

    def expire_old_requests(self,timestamp):
        c = self.conn.cursor()
        c.execute("""update service_requests set status = ? where (approved_at < ? and status = "APPROVED")""",("EXPIRED",timestamp))
    def commit(self):
        self.conn.commit()
    
    def rollback(self):
        self.conn.rollback()
    
    def close(self):
        self.conn.close()