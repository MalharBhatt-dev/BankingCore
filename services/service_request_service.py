import json
from datetime import datetime, timedelta


class ServiceRequestService:

    def __init__(self, repository, logger):
        self.repo = repository
        self.logger = logger


    def create_request(self, account_number, query_type, description):

        if not query_type:
            raise Exception("Query type required")

        try:

            self.repo.create_request(account_number, query_type, description)
            self.repo.commit()

            self.logger.info(
                f"Service request created by account {account_number}"
            )

        except Exception as e:
            self.repo.rollback()
            raise e


    def get_user_requests(self, account_number):

        rows = self.repo.get_user_requests(account_number)

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


    def get_pending_requests(self):

        rows = self.repo.get_pending_requests()

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


    def approve_request(self, request_id, employee_id):

        expires_at = (datetime.now() + timedelta(minutes=10)).isoformat()

        try:

            self.repo.approve_request(request_id, employee_id, expires_at)
            self.repo.commit()

            self.logger.info(
                f"Request {request_id} approved by employee {employee_id}"
            )

        except Exception as e:
            self.repo.rollback()
            raise e


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


    def submit_request(self, request_id, submission_data):

        try:

            data_json = json.dumps(submission_data)

            self.repo.submit_request(request_id, data_json)
            self.repo.commit()

            self.logger.info(
                f"Submission received for request {request_id}"
            )

        except Exception as e:
            self.repo.rollback()
            raise e