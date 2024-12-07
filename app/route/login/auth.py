from flask import Blueprint, request, current_app
from app.route.schema.input_schema_validate import AuthApi
from app.src.login.login import Auth
from app.src.util import Utils
from app.utils.timeit import timeit

auth_api = Blueprint(current_app.config["AUTH_ROUTE_NAME"], __name__)

@timeit
def _validate_schema(data: dict):
    """Validate the schema"""
    try:
        _schema_validate = AuthApi().load(data)
    except Exception as exc:
        error = Utils().get_error_number(exc, error_code=1001, service_code=1005)
        raise AssertionError(error)

@timeit
def get_request(request: request) -> dict:
    """
    Gets the requested input from request endpoint.

    Args:
        request (request): Input request

    Returns:
        dict: Record
    """
    try:
        if request.is_json:
            data = request.get_json()
            if not data:
                current_app.logger.info("Given request is the empty request")
                raise AssertionError(1008)
            _schema_validate = _validate_schema(data)
            return data
        else:
            raise AssertionError(1008)
    except Exception as exc:
        error = Utils().get_error_number(exc, service_code=1005)
        raise AssertionError(error)


@timeit
@auth_api.route(current_app.config["AUTH_ROUTE_NAME"], methods=["POST"])
def login():
    try:
        data = get_request(request)
        response = Auth().login(data)
        return response
    except Exception as exc:
        current_app.logger.critical("Error in login!")
        error = Utils().get_error_number(exc, service_code=1005)
        raise RuntimeError(error) from exc