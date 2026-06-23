from typing import Dict, Any, Union
import pandas as pd

from . import BaseClient, AuthMixin
from ..configs.env_var import BASE_URL, import_api_key

# es. "ODC-TBI-123"
DatasetID = Union[int, str]


class DatasetClient(BaseClient, AuthMixin):
    """
    Generic client.
    """

    def __init__(self, api_key: str = None):
        # check for api key in file
        if not api_key:
            try:
                api_key = import_api_key()
            except ValueError:
                raise ValueError("API Key not found! Check the .env file!")

        self.api_key = api_key

        # Init
        super().__init__(BASE_URL)
        AuthMixin.__init__(self, api_key)

    def _base_url_for(self, dataset_id: DatasetID) -> str:
        """URL Helper"""
        return f"{BASE_URL}/dataset/{dataset_id}"

    def info(self, dataset_id: DatasetID) -> Dict[str, Any]:
        """
        Get metadata.
        """
        url = f"{self._base_url_for(dataset_id)}/info"
        response = self._auth_get(url, self.api_key)
        return response.json() if hasattr(response, "json") else response

    def dictionary(self, dataset_id: DatasetID) -> Dict[str, Any]:
        """
        Get Data Dictionary.
        """
        url = f"{self._base_url_for(dataset_id)}/data-dictionary"
        response = self._auth_get(url, self.api_key)
        return response.json() if hasattr(response, "json") else response

    def data(self, dataset_id: DatasetID) -> Dict[str, Any]:
        """
        Get raw data!
        """
        url = self._base_url_for(dataset_id)
        response = self._auth_get(url, self.api_key)
        return response.json() if hasattr(response, "json") else response

    # --- Estensioni per Data Scientist (Pandas Integration) ---

    def data_df(self, dataset_id: DatasetID) -> pd.DataFrame:
        """Get pandas!"""
        raw_data = self.data(dataset_id)
        # Di solito le API SciCrunch restituiscono una lista di record o un dizionario con una chiave 'data'
        if isinstance(raw_data, dict) and "data" in raw_data:
            return pd.DataFrame(raw_data["data"])
        return pd.DataFrame(raw_data)

    def dictionary_df(self, dataset_id: DatasetID) -> pd.DataFrame:
        """Get metadata as pandas dataframe."""
        raw_dict = self.dictionary(dataset_id)
        if isinstance(raw_dict, dict) and "variables" in raw_dict:
            return pd.DataFrame(raw_dict["variables"])
        return pd.DataFrame(raw_dict)