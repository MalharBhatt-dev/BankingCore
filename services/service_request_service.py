import json
from datetime import datetime, timedelta


class ServiceRequestService:

    VALID_TRANSITIONS = {
    "PENDING": ["APPROVED", "REJECTED"],
    "APPROVED": ["SUBMITTED", "EXPIRED"],
    "SUBMITTED": ["COMPLETED"],
    "REJECTED": [],
    "COMPLETED": [],
    "EXPIRED": []
    }

    def __init__(self, repository, logger):
        self.repo = repository
        self.logger = logger


    def create_request(self, account_number, employee_id,query_type, description):

        if not query_type:
            raise Exception("Query type required")

        try:

            self.repo.create_request(account_number, employee_id ,query_type, description)
            self.repo.commit()

            self.logger.info(
                f"Service request created by account {account_number}"
            )

        except Exception as e:
            self.repo.rollback()
            raise e

    def get_requests_logs(self):
        rows = self.repo.get_requests_logs()
        result = []
        for r in rows:
            result.append({"request_id":r[1],
                           "account_number":r[2],
                           "submission_data":r[3],
                           "submitted_at":r[4]
                           })
        return result

    def get_user_requests(self, account_number):
        rows = self.repo.get_user_requests(account_number)
        result = []
        for r in rows:
            result.append({
                "id": r[0] if len(r) > 0 else None,
                "account_number": r[1] if len(r) > 1 else None,
                "query_type": r[2] if len(r) > 2 else None,
                "description": r[3] if len(r) > 3 else None,
                "status": r[4] if len(r) > 4 else None,
                "created_at": r[5] if len(r) > 5 else None,
                "employee_id":r[9] if len(r) > 9 else None
            })
        return result


    def get_pending_requests(self,account_number):

        rows = self.repo.get_pending_requests(account_number)

        result = []

        for r in rows:
            result.append({
                "id": r[0],
                "account_number": r[1],
                "query_type": r[2],
                "description": r[3],
                "status": r[4],
                "created_at": r[5]
            })

        return result


    def approve_request(self,request_id,employee_id):
        request = self.repo.get_request(request_id)
        current_status = request[4]
        self.validate_transition(current_status,"APPROVED")
        expires_at = (datetime.now()+timedelta(minutes=10)).isoformat()
        self.repo.approve_request(request_id,employee_id,expires_at)
        self.repo.commit()
        self.logger.info(
                f"Request {request_id} approved by employee {employee_id}"
            )


    def reject_request(self, request_id, employee_id):

        try:

            self.repo.reject_request(request_id, employee_id)
            self.repo.commit()

            self.logger.info(
                f"Request {request_id} rejected by employee {employee_id}"
            )

        except Exception as e:
            self.repo.rollback()
            raise e


    def submit_request(self,request_id,account_number,submission_data):

        request = self.repo.get_request(request_id)
        status = request[4]
        employee_id = request[6]
        expires_at = request[8]

        self.validate_transition(status,"SUBMITTED")

        if expires_at and datetime.now() > datetime.fromisoformat(expires_at):
            self.expire_requests()
            raise Exception("Request expired")

        data_json = json.dumps(submission_data)
        try:
            self.repo.submit_request(request_id,account_number,data_json,employee_id)
            self.repo.commit()
            self.logger.info(
                f"Request {request_id} submitted by account {account_number}"
            )
        except Exception as e:
            self.repo.rollback()
            raise e

    def complete_request(self,request_id):
        request = self.repo.get_request(request_id)
        account_number = request[1]
        status = request[4]
        self.validate_transition(status,"COMPLETED")
        try:
            self.repo.complete_request(request_id)
            self.repo.commit()
            self.logger.info(f"Request {request_id} completed by account {account_number}")
        except Exception as e:
            self.repo.rollback()
            raise e


    def validate_transition(self,current,new):
        allowed = self.VALID_TRANSITIONS.get(current,[])
        if new not in allowed:
            raise Exception(
                f"Invalid state transition: {current} → {new}"
            )
        
    def expire_requests(self):
        now = datetime.now().isoformat()
        self.repo.expire_old_requests(now)

    