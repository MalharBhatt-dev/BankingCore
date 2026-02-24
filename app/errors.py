from exceptions.base_exception import BankingException

def register_error_handlers(app):
    @app.errorhandler(BankingException)
    def handle_banking_exceptions(error):
        return{"error":str(error)},400
     
    @app.errorhandler(Exception)
    def handle_system_exceptions(error):
        print("system error",error)
        return{"error":"internal server error"},500