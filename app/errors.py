from exceptions.base_exception import BankingException

def register_error_handlers(app):
    @app.errorhandler(BankingException)
    def handle_banking_exceptions(error):
        return{"error":str(error)},400
     
    @app.errorhandler(BankingException)
    def handle_banking_exceptions(error):
        app.logger.warning(f"Business error: {str(error)}")
        return {"error": str(error)}, 400

    @app.errorhandler(Exception)
    def handle_system_exceptions(error):
        app.logger.error(f"System error: {str(error)}")
        return {"error": "Internal Server Error"}, 500
    
    @app.errorhandler(Exception)
    def handle_system_exceptions(error):
        app.logger.error(f"System error: {str(error)}")
        return {"error": "Internal Server Error"}, 500