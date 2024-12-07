from flask import current_app
from app.src.util import Utils
from app.utils.timeit import timeit
from app.src.elastic_middleware.search_data import SearchData
from datetime import datetime


class GetData:
    @timeit
    def get_current_date(self):
        try:
            current_app.logger.info("Current date fetching is begun!")
            date_time = datetime.now()
            epoch_time = int(date_time.timestamp())
            dt_object = datetime.utcfromtimestamp(epoch_time)
            return str(dt_object.date())
        except Exception as exc:
            current_app.logger.critical("Error in fetch the Bulk data!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc
    @timeit
    def preprocess_data(self, data_list):
        try:
            current_app.logger.info("preprocess_data is begun!")
            out = {}
            lst_data = []
            for data in data_list:
                out['date'] = data["_source"]['date']
                out['group'] = data["_source"]['group']
                out['id'] = data["_source"]['id']
                out['value'] = data["_source"]['value']
                lst_data.append(out)
            return lst_data
        except Exception as exc:
            current_app.logger.critical("Error in preprocess_data!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc   
    @timeit
    def get_tanker_or_bulk_data(self, role):
        try:
            current_app.logger.info("Bulk data fetching is begun!")
            data = SearchData().match_data_by_two_fields_no_size(Utils().read_variable_from_environment("ELASTIC_MARLO_DATA_INDEX"),"group",role, "date", self.get_current_date())
            response = self.preprocess_data(data)
            return response
        except Exception as exc:
            current_app.logger.critical("Error in fetch the Bulk data!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc

        
    @timeit
    def get_role_based_data(self, data):
        try:
            current_app.logger.info("check role is begun!")
            role = data[0]["_source"]['role']
            if role == "admin":
                tanker_data = self.get_tanker_or_bulk_data("tanker")
                bulk_data = self.get_tanker_or_bulk_data("bulk")
                return {"tanker_data": tanker_data, "bulk_data":bulk_data}
            elif role == "tanker":
                tanker_data = self.get_tanker_or_bulk_data(role)
                return {"tanker_data": tanker_data}
            elif role == "bulk":
                bulk_data = self.get_tanker_or_bulk_data(role)
                return {"bulk_data":bulk_data}
        except Exception as exc:
            current_app.logger.critical("Error in role checking!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc
        
    @timeit
    def get_data(self, data):
        try:
            current_app.logger.info("Data fetching is begun!")
            response = self.get_role_based_data(data)
            if response:
                return response
            return {"message":"Record not found!"}
        except Exception as exc:
            current_app.logger.critical("Error in fetch the data!")
            error = Utils().get_error_number(exc, service_code=1005)
            raise RuntimeError(error) from exc