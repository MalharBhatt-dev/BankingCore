from app.extensions import db
from app.models import ServiceRequest, RequestSubmission
from datetime import datetime


class ServiceRequestRepository:

    def create_request(self, account_number, employee_id, query_type, description):
        req = ServiceRequest(
            account_number=account_number,
            employee_id=employee_id,
            query_type=query_type,
            description=description,
            created_at=datetime.utcnow()
        )
        db.session.add(req)

    def get_requests_logs(self):
        return RequestSubmission.query.order_by(RequestSubmission.submitted_at).all()

    def get_user_requests(self, account_number):
        return ServiceRequest.query.filter_by(account_number=account_number)\
            .order_by(ServiceRequest.created_at.desc()).all()

    def get_pending_requests(self, employee_id):
        return ServiceRequest.query.filter_by(
            status="PENDING",
            employee_id=employee_id
        ).order_by(ServiceRequest.created_at.asc()).all()

    def get_request(self, request_id):
        return ServiceRequest.query.get(request_id)

    def approve_request(self, request_id, employee_id, expires_at):
        req = self.get_request(request_id)
        if req:
            req.status = "APPROVED"
            req.approved_by_employee = employee_id
            req.approved_at = datetime.utcnow()
            req.expires_at = expires_at

    def reject_request(self, request_id, employee_id):
        req = self.get_request(request_id)
        if req:
            req.status = "REJECTED"
            req.approved_by_employee = employee_id

    def submit_request(self, request_id, account_number, submission_data, employee_id):
        submission = RequestSubmission(
            request_id=request_id,
            account_number=account_number,
            submission_data=submission_data,
            submitted_at=datetime.utcnow()
        )
        db.session.add(submission)

        req = self.get_request(request_id)
        if req:
            req.status = "SUBMITTED"
            req.approved_by_employee = employee_id

    def complete_request(self, request_id):
        req = self.get_request(request_id)
        if req:
            req.status = "COMPLETED"

    def expire_old_requests(self, timestamp):
        requests = ServiceRequest.query.filter(
            ServiceRequest.status == "APPROVED",
            ServiceRequest.approved_at < timestamp
        ).all()

        for req in requests:
            req.status = "EXPIRED"

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()