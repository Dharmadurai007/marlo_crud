import os
import traceback
from datetime import datetime
from app.utils.timeit import timeit
from flask import current_app
from typing import Union


class Utils:
    @timeit
    def get_current_epoch_time(self) -> int:
        """Generates the epoch time for current datetime"""
        try:
            current_app.logger.info("Generate epoch time has begun!")
            date_time = datetime.now()
            epoch_time = int(date_time.timestamp())
            current_app.logger.info("Successfully get the epoch time!")
            return epoch_time
        except Exception as exc:
            current_app.logger.critical("Error in generate epoch time!")
            raise RuntimeError() from exc

    def read_variable_from_environment(self, variable_name: str):
        """Reads the variable from the os environment"""
        try:
            if variable_name not in os.environ:
                raise AssertionError(
                    6001, rf"Variable {variable_name} not found in env"
                )

            result = os.getenv(variable_name)
            if result == None or not result:
                raise KeyError(
                    6002,
                    rf"Variable {variable_name} is assigned with None or empty strings",
                )
            return result
        except Exception as exc:
            error = Utils().get_error_number(exc, service_code=6005)
            raise RuntimeError(error) from exc
    
    def read_credentials_from_environment(self, variable_name: str):
        """Reads the variable from the os environment"""
        result = ""
        try:
            if variable_name not in os.environ:
                print(fr"The {variable_name} is not loaded in the environment")

            result = os.getenv(variable_name)
            if result == None or not result:
                print(fr"The Variable {variable_name} is assigned with None or empty strings")
                result = ""
            return result
        except Exception as exc:
            print(fr"Error in reading the environment credential - {str(exc)}")
            print(traceback.format_exc())

       
    def _is_error_code(
        self,
        error: Exception,
        error_code: Union[int, str],
        service_code: Union[str, int],
    ):
        """Form error message body for error code"""
        if isinstance(error.args[0], dict) and "error_code" in error.args[0]:
            error_response = error.args[0]
        else:
            error_response = {
                "error_code": error_code,
                "error_message": str(error.args[0]),
                "service_error_code": service_code,
            }
        return error_response

    def _is_error_body(self, error: Exception, service_code: Union[str, int]):
        """Raise error for already constructed"""
        error_response = error.args[0]
        if "service_error_code" not in error_response:
            error_response["service_error_code"] = service_code
        return error_response

    def _get_messsage_for_error_code(
        self,
        error: Exception,
        error_code: Union[int, str],
        service_code: Union[str, int],
    ):
        """The raised exception has non integer error code"""
        if error_code:
            response = self._is_error_code(error, error_code, service_code)
        elif isinstance(error.args[0], dict):
            response = self._is_error_body(error, service_code)
        else:
            response = {"error_code": service_code, "error_message": "", "service_error_code": service_code}

        return response

    def _get_body_for_error_code(self, error: Exception, service_code: Union[str, int]):
        """Construct if it is integer error code"""
        error_response = {
            "error_code": error.args[0],
            "error_message": "",
            "service_error_code": service_code,
        }
        if len(error.args) == 2:
            error_response["error_message"] = error.args[1]
        return error_response

    def get_error_number(
        self, error: Exception, error_code: int = None, service_code: int = None
    ) -> Union[int, Exception]:
        "gets the error number from the exception"
        if len(error.args) > 0 and not isinstance(error.args[0], int):
            response = self._get_messsage_for_error_code(
                error, error_code, service_code
            )
        elif len(error.args) > 0 and isinstance(error.args[0], int):
            response = self._get_body_for_error_code(error, service_code)
        else:
            response = {"error_code": service_code, "error_message": "", "service_error_code": service_code}
        return response
