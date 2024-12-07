from config import Config
from app.data_connector import ElasticConnector
from app.src.util import Utils
from app.utils.timeit import timeit


class SearchData:
    def _generate_error_message(self, response: dict):
        """Generate custom error message based on elastic error"""
        try:
            status = response["status"]
            if status in Config.ELASTIC_ERROR_CODES:
                error_code = int(Config.ELASTIC_ERROR_CODES[status])
                raise RuntimeError(error_code)
            else:
                raise RuntimeError(2005)
        except Exception as exc:
            error = Utils().get_error_number(exc, service_code=2005)
            raise RuntimeError(error) from exc
    
    def get_total_record_count(self, index):
        try:
            response = ElasticConnector().count_index(index)
            if "error" in response:
                self._generate_error_message(response)
            elif response:
                return response["count"]
            else:
                raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, service_code=2005)
            raise RuntimeError(error) from exc
        
    def match_by_field_record_count(self, index, field, value):
        try:
            query = {"query": {"match_phrase": {field: value}}}
            response = ElasticConnector().count(index, query)
            if "error" in response:
                self._generate_error_message(response)
            elif response:
                return response["count"]
            else:
                raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, service_code=2005)
            raise RuntimeError(error) from exc
    
    def get_records(self, index: str, field: str, value: str, size: int = 1, start: int = 0) -> list:
        """Get datas from database if the string value matched

        Args:
            index (str): Elastic index name
            field (str): Field name
            value (str): Value to search
            size (int, optional): Size of the record to search. Defaults to 1.

        Returns:
            list: Resulted data
        """
        try:
            body = {"query": {"match_phrase": {field: value}}, "size": size, "from":start}
            response = ElasticConnector().search(index, body)
            if "error" in response:
                self._generate_error_message(response)
            elif len(response["hits"]["hits"]) != 0:
                return response["hits"]["hits"]
            else:
                raise ValueError(2006) 
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
        
    def get_all_records(self, index: str, size: int = 1, start: int = 0) -> list:
        """Get datas from database if the string value matched

        Args:
            index (str): Elastic index name
            field (str): Field name
            value (str): Value to search
            size (int, optional): Size of the record to search. Defaults to 1.

        Returns:
            list: Resulted data
        """
        try:
            body = {"query": {"match_all": {}}, "size": size, "from":start}
            response = ElasticConnector().search(index, body)
            if "error" in response:
                self._generate_error_message(response)
            elif len(response["hits"]["hits"]) != 0:
                return response["hits"]["hits"]
            else:
                raise ValueError(2006) 
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
        
    def delete_data(self, index: str, field: str, value: str) -> dict:
        """Delete data from database if the string value matched

        Args:
            index (str): Elastic index name
            field (str): Field name
            value (str): Value to search
            size (int, optional): Size of the record to search. Defaults to 1.

        Returns:
            list: Resulted data
        """
        try:
            body = {"query": {"match_phrase": {field: value}}}
            response = ElasticConnector().delete_by_query(index, body)
            if "error" in response:
                self._generate_error_message(response)
            return response 
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
        
    def is_exist_value(self, index: str, field: str, value: str, size: int = 1) -> bool:
        """Search data from database if the string value matched

        Args:
            index (str): Elastic index name
            field (str): Field name
            value (str): Value to search
            size (int, optional): Size of the record to search. Defaults to 1.

        Returns:
            list: Resulted data
        """
        try:
            body = {"query": {"match_phrase": {field: value}}, "size": size}
            response = ElasticConnector().search(index, body)
            if "error" in response:
                self._generate_error_message(response)
            elif response["hits"]["hits"]:
                return True
            return False
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
        
    @timeit
    def match_data_by_two_fields_is_exist(
        self, index_name, field1: str, value1: str, field2: str, value2: str
    ):
        """Search data if all two values matched

        Args:
            index_name (str): Elastic index name
            field1 (str): First field to search
            value1 (any): First field value
            field2 (str): Second field to search
            value2 (str): Second field value
        Returns:
            list: Matched records
        """
        try:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match_phrase": {field1: value1}},
                            {"match_phrase": {field2: value2}},
                        ]
                    }
                }
            }
            response = ElasticConnector().search(index_name, query)
            if "error" in response:
                self._generate_error_message(response)
            elif response["hits"]["hits"]:
                return True
            return False
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
        
    def match_by_all(self, index: str, field: str, value: str) -> list:
        """Search data from database if the string value matched

        Args:
            index (str): Elastic index name
            field (str): Field name
            value (str): Value to search
            size (int, optional): Size of the record to search. Defaults to 1.

        Returns:
            list: Resulted data
        """
        try:
            body = {"query": {"match_phrase": {field: value}}}
            response = ElasticConnector().search(index, body)
            if "error" in response:
                self._generate_error_message(response)
            elif "error" not in response:
                return response["hits"]["hits"]
            else:
                raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
            
    def match_by_field(self, index: str, field: str, value: str, size: int = 1) -> list:
        """Search data from database if the string value matched

        Args:
            index (str): Elastic index name
            field (str): Field name
            value (str): Value to search
            size (int, optional): Size of the record to search. Defaults to 1.

        Returns:
            list: Resulted data
        """
        try:
            body = {"query": {"match_phrase": {field: value}}, "size": size}
            response = ElasticConnector().search(index, body)
            if "error" in response:
                self._generate_error_message(response)
            elif len(response["hits"]["hits"]) != 0:
                return response["hits"]["hits"]
            else:
                raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
        
    def get_identity(self, doc_name:str) -> int:
        try:
            response = self.search_all_data("identity")
            for record in response:
                if doc_name in record['_source']:
                    identity_value = record["_source"][doc_name]["identity"]
                    self.update_identity(doc_name, identity_value)
            return identity_value
        except Exception as exc:
            error = Utils().get_error_number(exc, service_code=2005)
            raise RuntimeError(error) from exc
        
    def update_identity(self, doc_name, current_identity):
        try:
            response = self.search_all_data("identity")
            for record in response:
                if doc_name in record['_source']:
                    record["_source"][doc_name]["identity"] = current_identity + 1
                    response = self.update_document("identity",record['_source'], record["_id"])
            return response
        except Exception as exc:
            error = Utils().get_error_number(exc, service_code=2005)
            raise RuntimeError(error) from exc

    @timeit
    def match_by_field_numbers(
        self, index: str, field: str, value: str, size: int = 1
    ) -> list:
        """Search records by single field value"""
        body = {"query": {"match": {field: value}}, "size": size}
        response = ElasticConnector().search(index, body)
        return response["hits"]["hits"]

    @timeit
    def search_all_data(self, index: str) -> list:
        """Search all records by field value"""
        body = {"query": {"match_all": {}}, "size": 10000}
        response = ElasticConnector().search(index, body)
        return response["hits"]["hits"]

    @timeit
    def match_data_by_two_fields_by_matchphrase(
        self, index_name, field1: str, value1: str, field2: str, value2: str, size: int, start: int
    ):
        """Search data if all two values matched

        Args:
            index_name (str): Elastic index name
            field1 (str): First field to search
            value1 (any): First field value
            field2 (str): Second field to search
            value2 (str): Second field value
        Returns:
            list: Matched records
        """
        try:
            query = {
                    "query": {
                        "bool": {
                            "must": [
                                {
                                    "match_phrase_prefix": {
                                        field1: {
                                            "query": value1
                                        }
                                    }
                                },
                                {
                                    "match_phrase": {
                                        field2: value2
                                    }
                                }
                            ]
                        }
                        },
                    "size": size, "from":start
                    }
            response = ElasticConnector().search(index_name, query)
            if "error" in response:
                self._generate_error_message(response)
            elif len(response["hits"]["hits"]) != 0:
                return response["hits"]["hits"]
            else:
                raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, service_code=2005)
            raise RuntimeError(error) from exc

    @timeit
    def match_data_by_two_fields(
        self, index_name: str, field1: str, value1: any, field2: str, value2: any, size: int = 1
    ):
        """Search data if all two values matched

        Args:
            index_name (str): Elastic index name
            field1 (str): First field to search
            value1 (any): First field value
            field2 (str): Second field to search
            value2 (any): Second field value
        Returns:
            list: Matched records
        """
        try:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match_phrase": {field1: value1}},
                            {"match_phrase": {field2: value2}},
                        ]
                    }
                },
                "size": size,
            }
            response = ElasticConnector().search(index_name, query)
            if "error" in response:
                self._generate_error_message(response)
            elif len(response["hits"]["hits"]) != 0:
                return response["hits"]["hits"]
            raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
        

    def match_data_by_three_field_by_matchphrase(
        self, index_name, field1, value1, field2, value2, field3, value3
    ):
        try:
            query = {
                "query": {
                    "bool": {
                        "must": [
                            {"match": {field1: value1}},
                            {"match": {field2: value2}},
                            {"match_phrase": {field3: value3}},
                        ]
                    }
                },
                "size": 10000,
            }
            response = ElasticConnector().search(index_name, query)
            if "error" in response:
                self._generate_error_message(response)
            elif len(response["hits"]["hits"]) != 0:
                return response["hits"]["hits"]
            else:
                raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc

    @timeit
    def match_data_by_four_field_by_matchphrase(
        self,
        index_name: str,
        field1: str,
        value1: any,
        field2: str,
        value2: any,
        field3: str,
        value3: any,
        field4: str,
        value4: str,
    ) -> list:
        """Search data if all four values matched

        Args:
            index_name (str): Elastic index name
            field1 (str): First field to search
            value1 (any): First field value
            field2 (str): Second field to search
            value2 (any): Second field value
            field3 (str): Third field to search
            value3 (any): Third field value
            field4 (str): Fourth field value to search
            value4 (str): Fourth field value

        Returns:
            list: Matched records
        """
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {field1: value1}},
                        {"match": {field2: value2}},
                        {"match": {field3: value3}},
                        {"match_phrase": {field4: value4}},
                    ]
                }
            },
            "size": 10000,
        }
        response = ElasticConnector().search(index_name, query)
        return response["hits"]["hits"]

    @timeit
    def match_data_by_three_field(
        self,
        index_name: str,
        field1: str,
        value1: any,
        field2: str,
        value2: any,
        field3: str,
        value3: any,
    ):
        """Search data if all three values matched

        Args:
            index_name (str): Elastic index name
            field1 (str): First field to search
            value1 (any): First field value
            field2 (str): Second field to search
            value2 (any): Second field value
            field3 (str): Third field to search
            value3 (any): Third field value

        Returns:
            list: Matched records
        """
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {field1: value1}},
                        {"match": {field2: value2}},
                        {"match": {field3: value3}},
                    ]
                }
            },
            "size": 10000,
        }
        response = ElasticConnector().search(index_name, query)
        return response["hits"]["hits"]

    @timeit
    def update_identity_record(self, identity: int) -> dict:
        """Construct the schema to update the identity number

        Args:
            identity (int): latest identity number

        Returns:
            dict: Constructed document
        """
        body = {"doc": {"identity": identity + 1}}
        return body

    def update_document(self, index_name, body, id):

        try:
            schema = {"doc": body}
            response = ElasticConnector().update_doc(index_name, schema, id)
            if "error" in response:
                self._generate_error_message(response)
            return response
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc

    @timeit
    def get_random_questions(self, index_name, question_count, sub_skill):
        try:
            query = {
                "size": question_count,  # Number of documents to retrieve
                "from": 0,  # Starting point of the search
                "query": {
                    "function_score": {
                        "query": {"match": {"sub_skill_pack_name": sub_skill}},
                        "random_score": {},
                    }
                },
            }
            response = ElasticConnector().search(index_name, query)
            if "error" in response:
                self._generate_error_message(response)
            elif len(response["hits"]["hits"]) != 0:
                return response["hits"]["hits"]
            else:
                raise ValueError(2006)
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc

    @timeit
    def match_with_range_query(self, field, value, range_field, range_value):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {field: value}},
                        {"range": {range_field: {"gt": range_value}}},
                    ]
                }
            }
        }
        return query

    @timeit
    def question_construct_by_category(self, field, value, size):
        construct_query = {
            "bool": {"must": [{"match": {field: value}}], "minimum_should_match": size}
        }
        return construct_query

    @timeit
    def sort_queries_by_match_field(
        self, index_name, field1, value1, field2, value2, sort_field, sort_value
    ):
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {field1: value1}},
                        {"match": {field2: value2}},
                    ]
                }
            },
            "sort": [{sort_field: {"order": sort_value}}],
            "size": 1,
        }
        response = ElasticConnector().search(index_name, query)
        return response["hits"]["hits"]

    @timeit
    def search_unique_fields(self, index_name, field):
        """Search data by unique fields"""
        query = {"size": 0, "aggs": {"item": {"terms": {"field": field, "size": 1000}}}}
        response = ElasticConnector().search(index_name, query)
        return response["aggregations"]["item"]["buckets"]

    @timeit
    def match_all_query(self, index_name):
        """MAtch all query"""
        query = {"query": {"match_all": {}}, "size": 10000}
        response = ElasticConnector().search(index_name, query)
        return response["hits"]["hits"]

    @timeit
    def match_data_by_two_fields_no_size(
        self, index_name, field1, value1, field2, value2
    ):
        """search records if two values matched"""
        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {field1: value1}},
                        {"match": {field2: value2}},
                    ]
                }
            },
        }
        response = ElasticConnector().search(index_name, query)
        return response["hits"]["hits"]

    

    @timeit
    def latest_record_by_created_date(self, index_name: str):
        search_query = {
            "query": {"match_all": {}},
            "sort": [{"id": {"order": "desc"}}],
            "size": 1,
        }
        response = ElasticConnector().search(index_name, search_query)
        if "error" not in response:
            return response["hits"]["hits"]
        else:
            return []

    def refresh_index(self, index_name: str) -> None:
        try:
            response = ElasticConnector().refresh_index(index_name)
            if "error" in response:
                self._generate_error_message(response)
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc

    def insert_document(self, index_name: str, input_data: dict, doc_id: str = ""):
        try:
            response = ElasticConnector().insert_doc(index_name, input_data, doc_id)
            if "error" in response:
                self._generate_error_message(response)
            return response
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
    
    def get_document(self, index_name: str, doc_id: str):
        try:
            response = ElasticConnector().get_doc(index_name, doc_id)
            if "error" in response:
                self._generate_error_message(response)
            return response
        except Exception as exc:
            error = Utils().get_error_number(exc, error_code=2007, service_code=2005)
            raise RuntimeError(error) from exc
