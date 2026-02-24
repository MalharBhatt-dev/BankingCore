from exceptions.base_exception import BankingException
from exceptions.token_expired_exception import TokenExpiredException
from exceptions.invalid_token_exception import InvalidTokenException
def register_error_handlers(app):
    @app.errorhandler(BankingException)
    def handle_banking_exceptions(error):
        return{"error":str(error)},400
     
    @app.errorhandler(BankingException)
    def handle_banking_exceptions(error):
        app.logger.warning(f"Business error: {str(error)}")
        return {"error": str(error)}, 400
    
    @app.errorhandler(TokenExpiredException)
    def handle_token_expired(error):
        app.logger.warning("Expired token used.")
        return  {"error":str(error)},401
    
    @app.errorhandler(InvalidTokenException)
    def handle_invalid_token(error):
        app.looger.warning("Invalid token used.")
        return {"error":str(error)},401

    @app.errorhandler(Exception)
    def handle_system_exceptions(error):
        app.logger.error(f"System error: {str(error)}")
        return {"error": "Internal Server Error"}, 500
    
 