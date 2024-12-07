from typing import List, Dict
from urllib import response
import requests
import json
from requests.auth import HTTPBasicAuth
import warnings
from app.utils.timeit import timeit
from app.src.util import Utils

warnings.filterwarnings("ignore")


class ElasticConnector:
    """
    A Class that establish connection to Elasticsearch, perform creation,insertion,updation and deletion operations.

    Parameters
    ----------
     url : str
            Input url as string.
     username : str
            Input username as string.
     password : str
            Input password as string.

    Methods
    -------
    index_exists(index_name: str)
         Checks if the index name exists in the instance.

    id_exists(index_name: str,doc_id: str)
        Checks if the document id exists in the index

    get_indices()
         Lists all the indices that are created.

    refresh_index(index_name: str)
         Refresh the index upon request

    create_index(index_name: str,schema: dict = {})
         Creates the index with the name and schema provided

    update_settings(index_name: str,settings: dict)
          Allows to update the settings for the index given

    update_mapping(index_name: str,mapping: dict)
          Mapping / addition of fields to the index can be done using this method.

    clone_index(source_index: str, target_index: str)
          Clones the source index into the target index with all the mappings, settings, data retained.

    delete_index(index_name: str)
         Deletes the index with the name given.

    insert_doc(index_name: str,input_data: dict,doc_id: str = "")
           Inserts the document with the schema and id provided in the index.

    update_doc(index_name: str,schema: dict,doc_id: str)
           Updates the document with the schema and id provided.

    get_doc(index_name: str,doc_id: str)
           This method returns the document matching the ID given as input.

    delete_doc(index_name: str,doc_id: str)
         Document matching the given id will be deleted with this method.

    search(index_name: str,query: dict)
         Return the documents that matches the query given
    """

    def __init__(
        self,
        url: str = Utils().read_credentials_from_environment("ELASTIC_IP"),
        username: str = Utils().read_credentials_from_environment("ELASTIC_USERNAME"),
        password: str = Utils().read_credentials_from_environment("ELASTIC_PASSWORD"),
    ) -> None:
        """
        Establish an elastic connection with the username and password

        Parameters
        ----------
        url : str
            Input url as string.
        username : str
            Input username as string.
        password : str
            Input password as string.

        """
        if isinstance(url, str):
            self.base_url: str = url
        else:
            raise ValueError("Invalid data type. Given url must be string.")
        if isinstance(username, str):
            self.username: str = username
        else:
            raise ValueError("Invalid data type. Given username must be string.")
        if isinstance(password, str):
            self.password: str = password
        else:
            raise ValueError("Invalid data type. Given password must be string.")

        self.headers = {"content-type": "application/json", "charset": "UTF-8"}
        self.auth = HTTPBasicAuth(self.username, self.password)

        self.doc = "/_doc/"

    @timeit
    def index_exists(self, index_name: str) -> bool:
        """
        This method checks if the index exists

        Parameters:
        ----------
        index_name: str
           Name of the index to validate

        Returns:
        ----------
        bool: Returns True if the index exists, else it returns False
        """
        status = requests.head(self.base_url + index_name, auth=self.auth)
        return status.status_code == 200

    @timeit
    def id_exists(self, index_name: str, doc_id: str) -> bool:
        """
        This method checks if the id exists in the index

        Parameters:
        ----------
        index_name: str
            index_name to check the document ID
        doc_id:  str
            The actual document id to check the record

        Returns:
        ----------
        bool: Returns True if the id exists in the index, else False is returned
        """
        status = requests.head(
            self.base_url + index_name + self.doc + doc_id,
            headers=self.headers,
            auth=self.auth,
        )
        return status.status_code == 200

    @timeit
    def get_indices(self) -> List:
        """
        This method returns the indices that belong to the Elastic DB

        Returns:
        ----------
        List: Returns all the index names.
        """

        index_names = requests.get(
            self.base_url + "_cat/indices?h=index", auth=self.auth
        )
        indices = index_names.text.split("\n")
        indices = [index for index in indices if index]
        return indices

    def refresh_index(self, index_name: str) -> response:
        """
        This method is to refresh the index upon request.

        Parameters:
        ----------
        index_name: str
            index_name to refresh.

        Returns:
        ----------
        None

        """
        response = requests.post(
            self.base_url + index_name + "/_refresh", auth=self.auth
        )
        return response

    @timeit
    def create_index(self, index_name: str, schema: dict = {}) -> Dict:
        """
        This method creates the index with the schema provided.

        Parameters:
        ----------
        index_name: str
            index_name to update the index with mappings.
        schema: dict
            This contains the mapping with the field names, normalizers, settings etc.

        Returns:
        ----------
        dict: Returns elastic index creation status.

        """

        creation_status = requests.put(
            self.base_url + index_name,
            data=json.dumps(schema),
            headers=self.headers,
            auth=self.auth,
        )
        return creation_status.json()

    @timeit
    def update_settings(self, index_name: str, settings: dict) -> Dict:
        """
        This method updates the settings for the index.

        Parameters:
        ----------
        index_name: str
            index_name to update the index with settings
        settings: dict
            This contains the neccessary parameters as part of settings

        Returns:
        ----------
        Dict: The status on settings update is shown.

        """
        setting_status = requests.put(
            self.base_url + index_name + "/_settings",
            data=json.dumps(settings),
            headers=self.headers,
            auth=self.auth,
        )
        return setting_status.json()

    @timeit
    def update_mapping(self, index_name: str, mapping: dict) -> Dict:
        """
        This method updates the mapping for the index created.

        Parameters:
        ----------
        index_name: str
            index_name to update the index with mapping
        mapping: dict
            This contains the necessary parameters as part of mapping [Fields and associated type]

        Returns:
        ----------
        Dict: Mapping update status is returned as JSON response.

        """
        mapping_status = requests.put(
            self.base_url + index_name + "/_mapping",
            data=json.dumps(mapping),
            headers=self.headers,
            auth=self.auth,
        )
        return mapping_status.json()

    @timeit
    def clone_index(self, source_index: str, target_index: str) -> Dict:
        """
        This method clones the index from the source index.

        Parameters:
        ----------
        source_index: str
           source index to clone the mappings, settings and data
        target_index: str
            target index to be cloned from source index

        Returns:
        ----------
        dict: Returns index clone status as output

        """
        clone_status = requests.post(
            self.base_url + source_index + "/_clone/" + target_index,
            headers=self.headers,
            auth=self.auth,
        )
        return clone_status.json()

    @timeit
    def delete_index(self, index_name: str) -> Dict:
        """
        Method to delete the Elasticsearch Index.

        Parameters:
        ----------
        index_name: str
            index_name to delete.

        Returns:
        ----------
        Dict: Status on the index deletion
        """
        delete_status = requests.delete(self.base_url + index_name, auth=self.auth)
        return delete_status.json()

    def insert_doc(self, index_name: str, input_data: dict, doc_id: str = ""):
        """
        Method to insert the document to Elasticsearch Index.

        Parameters:
        ----------
        index_name: str
            index_name to insert the document
        input_data: dict
            The actual document with the necessary fields
        doc_id: dict
            The document id to assign the document with unique identification.

        Returns:
        ----------
        Dict: Document insertion status is given as response.
        """

        doc_id = "/" + doc_id if doc_id != "" else doc_id
        insert_status = requests.post(
            self.base_url + index_name + "/_doc" + doc_id,
            data=json.dumps(input_data),
            headers=self.headers,
            auth=self.auth,
        )
        return insert_status.json()

    def update_doc(self, index_name: str, schema: dict, doc_id: str) -> Dict:
        """
        Method to update the document in Elasticsearch Index.

        Parameters:
        ----------
        index_name: str
            index_name to update the document
        schema: dict
            The document to update in elastic index
        doc_id: str
            Document ID to update the record

        Returns:
        ----------
        Dict: Document updation status as response.
        """
        updation_status = requests.post(
            self.base_url + index_name + "/_update/" + doc_id,
            data=json.dumps(schema),
            headers=self.headers,
            auth=self.auth,
        )
        return updation_status.json()

    def get_doc(self, index_name: str, doc_id: str):
        """
        Method to get the document from Elasticsearch Index.

        Parameters:
        ----------
        index_name: str
            index_name to get the document
        doc_id: str
            Document ID to get the record

        Returns:
        ----------
        Dict: Returns the document matching the id.
        """
        documents = requests.get(
            self.base_url + index_name + self.doc + doc_id,
            headers=self.headers,
            auth=self.auth,
        )
        return documents.json()

    @timeit
    def delete_doc(self, index_name: str, doc_id: str) -> Dict:
        """
        Method to delete the document from Elasticsearch Index.

        Parameters:
        ----------
        index_name: str
            index_name to delete the document
        doc_id: str
            Document ID to delete the record

        Returns:
        ----------
        Dict: Document deletion status as response.
        """
        delete_status = requests.delete(
            self.base_url + index_name + self.doc + doc_id, auth=self.auth
        )
        return delete_status.json()

    def search(self, index_name: str, query: dict) -> Dict:
        """
        Method to search for the documents that matches criteria

        Parameters:
        ----------
        index_name: str
            index_name to look for the documents
        query: str
            Filter criteria as query parameters

        Returns:
        ----------
        Dict: Documents that matches the query.
        """
        search_results = requests.post(
            self.base_url + index_name + "/_search/",
            data=json.dumps(query),
            headers=self.headers,
            auth=self.auth,
        )
        return search_results.json()
    
    def delete_by_query(self, index_name: str, query: dict) -> Dict:
        """
        Method to delete for the documents that matches criteria

        Parameters:
        ----------
        index_name: str
            index_name to look for the documents
        query: str
            Filter criteria as query parameters

        Returns:
        ----------
        Dict: Documents that matches the query.
        """
        delete_results = requests.post(
            self.base_url + index_name + "/_delete_by_query/",
            data=json.dumps(query),
            headers=self.headers,
            auth=self.auth,
        )
        return delete_results.json()

    @timeit
    def count(self, index_name: str, query: dict) -> Dict:
        """
        Method to find the total number of record in elastic

        Parameters:
        ----------
        index_name: str
            index_name to look for the documents
        query: str
            Filter criteria as query parameters

        Returns:
        ----------
        Dict: Total count.
        """
        count_result = requests.post(
            self.base_url + index_name + "/_count",
            data=json.dumps(query),
            headers=self.headers,
            auth=self.auth,
        )
        return count_result.json()

    @timeit
    def count_index(self, index_name: str) -> Dict:
        """
        Method to find the total number of record in elastic

        Parameters:
        ----------
        index_name: str
            index_name to look for the documents
        query: str
            Filter criteria as query parameters

        Returns:
        ----------
        Dict: Total count.
        """
        count_result = requests.post(
            self.base_url + index_name + "/_count",
            headers=self.headers,
            auth=self.auth,
        )
        return count_result.json()

    
