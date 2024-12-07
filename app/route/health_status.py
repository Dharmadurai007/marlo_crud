from flask import Blueprint

health_status_api = Blueprint("/", __name__)


@health_status_api.route("/", methods=["GET"])
def health_status():
    """
    Checks the Health status of the code for load balancer.
    """
    return {"status": 200}
