from app.utils.timeit import timeit
from flask import current_app
from app.src.util import Utils
from app.src.elastic_middleware.search_data import SearchData
from app.utils.encryption import encrypt
from app.src.data_crud.get_data import GetData


class Auth:
    
    @timeit
    def check_password(self, data, response):
        try:
            current_app.logger.info("Password checking!")
            if "password" in data:
             if data['password'] == response[0]["_source"]['password']:
                role = response[0]["_source"]['role']
                output = GetData().get_data(response)
                return output
             raise AssertionError(1007)
            raise AssertionError(1010)
        except Exception as exc:
            current_app.logger.critical("Error in login passsword check!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc
    
    @timeit
    def check_role(self, data, response):
        try:
            current_app.logger.info("Role checking!")
            if response:
                return self.check_password(data, response)
            return {"message": "You login the user is not existed!"}
        except Exception as exc:
            current_app.logger.critical("Error in login role check!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc
        
    
    @timeit
    def get_user_data(self, is_admin_user, email_id):
        try:
            current_app.logger.info("Get user data is begun!")
            if is_admin_user:
                response = SearchData().match_by_field(Utils().read_variable_from_environment("ELASTIC_ADMIN_USERS_INDEX"),"email_id",email_id)
                if response[0]['_source']['role'] == "client":
                    if self._is_client_link_expired(response[0]['_source']['id']):
                        return {"message":"Your link has been expired!. Please contact your Admin."}
                    return {"message": encrypt("Successfully login!"), "user_id":response[0]['_source']["id"], "role":response[0]['_source']["role"]}        
                return {"message": encrypt("Successfully login!"), "user_id":response[0]['_source']["id"], "role":response[0]['_source']["role"]}
            else:
                response = SearchData().match_by_field(Utils().read_variable_from_environment("ELASTIC_CLIENT_USERS_INDEX"),"email_id",email_id)
                if self._is_client_link_expired(response[0]['_source']['client_id']):
                    return {"message":"Your link has been expired!. Please contact your Admin."}
                return {"message": encrypt("Successfully login!"), "user_id":response[0]['_source']["client_id"], "role":"client"}
        except Exception as exc:
            current_app.logger.critical("Error in fetch the user data!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc
        
    @timeit
    def login(self, data):
        try:
            current_app.logger.info("Login is begun!")
            email_id = data["email_id"]
            is_user = SearchData().is_exist_value(Utils().read_variable_from_environment("ELASTIC_MARLO_USERS_INDEX"),"email_id",email_id)
            if is_user:
                response = SearchData().match_by_field(Utils().read_variable_from_environment("ELASTIC_MARLO_USERS_INDEX"),"email_id",email_id)
                return self.check_role(data, response)
            raise AssertionError(1006)
        except Exception as exc:
            current_app.logger.critical("Error in login!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc            


