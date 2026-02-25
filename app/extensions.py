from flask import g
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


limiter = Limiter(key_func = lambda:getattr(g,"account_number",get_remote_address),default_limits=["100 per hour"])