from . import BaseClient, AuthMixin
from ..configs.env_var import BASE_URL


class DatasetClient(BaseClient, AuthMixin):
    def __init__(self, api_key: str, dataset_id: int):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key

        if not dataset_id:
            raise ValueError("dataset_id is required")
        self.dataset_id = dataset_id

        super().__init__(BASE_URL)
        AuthMixin.__init__(self, api_key)

    def _base(self):
        return f"{BASE_URL}/dataset/{self.dataset_id}"

    def info(self):
        return self._auth_get(f"{self._base()}/info/", self.api_key)

    def data(self):
        return self._auth_get(self._auth_url(self._base()), self.api_key)

    def dictionary(self):
        return self._auth_get(f"{self._base()}/data-dictionary/", self.api_key)
