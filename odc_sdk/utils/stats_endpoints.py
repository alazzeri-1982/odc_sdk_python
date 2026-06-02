from typing import List, Dict, Any, Literal
from dataclasses import asdict
import pandas as pd

from ..configs.env_var import BASE_URL
from .request_handler import RequestHandler
from ..models.stats_responses import (
    UserStat,
    DatasetStat,
    LabStat,
    DownloadStat,
)

StatType = Literal["users", "datasets", "labs", "downloads"]


class StatsClient:
    """
    Fixed-schema typed SDK client.
    Uses dataclasses directly (no registration, no generics).
    """

    def __init__(self):
        self._handler = RequestHandler()

        # hard-bound endpoint map
        self._endpoints: Dict[StatType, str] = {
            "users": f"{BASE_URL}/stats/users",
            "datasets": f"{BASE_URL}/stats/datasets",
            "labs": f"{BASE_URL}/stats/labs",
            "downloads": f"{BASE_URL}/stats/downloads",
        }

        # hard-bound model map (dataclasses only)
        self._models = {
            "users": UserStat,
            "datasets": DatasetStat,
            "labs": LabStat,
            "downloads": DownloadStat,
        }

    # core fetch
    def _fetch(self, stat: StatType, retries: int = 3, delay: int = 10) -> List[Any]:
        model = self._models[stat]
        endpoint = self._endpoints[stat]

        response = self._handler.get_response(endpoint, retries=retries, delay=delay)

        if response.status_code != 200:
            raise RuntimeError(
                f"Request failed for '{stat}' (status={response.status_code})"
            )

        data = response.json()
        return [model(**item) for item in data]

    # typed API
    def users(self, **kwargs) -> List[UserStat]:
        return self._fetch("users", **kwargs)

    def datasets(self, **kwargs) -> List[DatasetStat]:
        return self._fetch("datasets", **kwargs)

    def labs(self, **kwargs) -> List[LabStat]:
        return self._fetch("labs", **kwargs)

    def downloads(self, **kwargs) -> List[DownloadStat]:
        return self._fetch("downloads", **kwargs)

    def get(self, stat: StatType, **kwargs):
        return self._fetch(stat, **kwargs)

    # DataFrame export
    def to_dataframe(self, stat: StatType, **kwargs) -> pd.DataFrame:
        records = self._fetch(stat, **kwargs)

        return pd.DataFrame([asdict(r) for r in records])

    # convenience shortcuts
    def users_df(self, **kwargs) -> pd.DataFrame:
        return self.to_dataframe("users", **kwargs)

    def datasets_df(self, **kwargs) -> pd.DataFrame:
        return self.to_dataframe("datasets", **kwargs)

    def labs_df(self, **kwargs) -> pd.DataFrame:
        return self.to_dataframe("labs", **kwargs)

    def downloads_df(self, **kwargs) -> pd.DataFrame:
        return self.to_dataframe("downloads", **kwargs)
