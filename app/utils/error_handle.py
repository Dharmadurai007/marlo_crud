from flask import Flask
from typing import Union
from app.utils.timeit import timeit


class ErrorHandle:
    @timeit
    def _get_error_series(self, app: Flask, error_code: Union[str, int]) -> str:
        """Find which error series it has"""
        error_series = ""
        if error_code and isinstance(error_code, int):
            error_series = app.config["ERROR_CODE_SERIES"][int(str(error_code)[:2])]
        return error_series

    @timeit
    def _form_error_response(
        self,
        app: Flask,
        error_code: Union[str, int],
        error_series: str,
        error_message: str,
        service_error_code: Union[int, str],
    ):
        """Construct the error response"""
        custom_message_body = {}
        if error_code and error_series and error_code in app.config[error_series]:
            custom_error_message = app.config[error_series][error_code]
            custom_message_body.update(custom_error_message)
            if not custom_message_body["internal_message"] and error_message:
                custom_message_body["internal_message"] = error_message
            return {"error_code": error_code, "error_message": custom_message_body}
        elif service_error_code and error_series:
            custom_error_message = app.config[error_series][service_error_code]
            custom_message_body.update(custom_error_message)
            return {
                "error_code": service_error_code,
                "error_message": custom_message_body,
            }
        else:
            custom_message_body = {
                "error_code": 9005,
                "error_message": {
                    "internal_message": "Unknown error",
                    "external_message": "Unable to process the request",
                },
            }

        return custom_message_body

    @timeit
    def handle_error(self, app: Flask, error: Exception) -> dict:
        """Handle the custom error message based on error code

        Args:
            app (Flask): context manager
            error (Exception): error code and custom message

        Returns:
            dict: Error response
        """
        if len(error.args) > 0 and isinstance(error.args[0], dict):
            error_body = error.args[0]
            error_code = error_body.get("error_code", "")
            service_error_code = error_body.get("service_error_code", "")
            error_message = error_body.get("error_message", "")

            error_series = self._get_error_series(app, error_code)

            custom_error = self._form_error_response(
                app, error_code, error_series, error_message, service_error_code
            )
            return custom_error
        return {
                "error_code": 9005,
                "error_message": {
                    "internal_message": "Unknown error",
                    "external_message": "Unable to process the request",
                },
            }
