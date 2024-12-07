import os
import traceback
from flask_cors import CORS
from config import Config
from dotenv import load_dotenv
from flask import Flask
from app.utils import init_logger
from flask_wtf.csrf import CSRFProtect
from app.utils import ErrorHandle

load_dotenv()
def create_app() -> Flask:
    """
    Initialize the flask application.

    Args:
        config (str): The environment config parameters.

    Returns:
        Flask: Flask app.
    """
    app = Flask(__name__, instance_relative_config=False)
    csrf = CSRFProtect()
    app.config['DEBUG'] = True
    CORS(app=app, methods=['POST','GET'], resources={Config.ROUTE_ENDPOINT_PATTERN: {"origins": Config.DOMAIN_ORIGIN, "send_wildcard": Config.IS_CORS_ENABLED}})
    csrf.init_app(app)
    config = os.getenv('FLASK_ENV', 'DevConfig')
    app.config.from_object(rf"config.{config}")
    with app.app_context():
        configure_logging(app)
        register_error_handlers(app)
        register_blueprints(app)
    return app


def configure_logging(app: Flask) -> None:
    """
    Initializing the log file.

    Args:
        app (Flask): Flask app
    """
    init_logger(app)


def register_error_handlers(app: Flask) -> None:
    """
    Register error handlers with application context

    Args:
        app (Flask): Flask app
    """            

    @app.errorhandler(Exception)

    def handle_exception(errors):
        """Return custom JSON when APIError or its children are raised"""
        app.logger.critical(rf"Error in config service - {str(errors)}")
        app.logger.debug(traceback.format_exc())
        response = ErrorHandle().handle_error(app, errors)
        return response

def register_blueprints(app: Flask) -> None:
    """
    Register the blueprint endpoint to application context

    Args:
        app (Flask): Flask app.
    """
    from app.route import health_status_api
    from app.route.login import auth_api
    
    app.register_blueprint(health_status_api)
    app.register_blueprint(auth_api)

    