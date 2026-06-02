from . import BaseClient, AuthMixin
from ..configs.env_var import BASE_URL


class UserClient(BaseClient, AuthMixin):
    def __init__(self, api_key: str):
        if not api_key:
            raise ValueError("api_key is required")
        self.api_key = api_key

        BaseClient.__init__(self, BASE_URL)
        AuthMixin.__init__(self, api_key)

    def info(self):
        url = self._auth_url(f"{BASE_URL}/user/info/")
        return self._auth_get(url, self.api_key)
