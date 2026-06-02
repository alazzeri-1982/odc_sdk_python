import time
import requests
import pandas as pd
import json
from typing import Type, TypeVar, Any

T = TypeVar("T")


class RequestHandler:
    # basic retry default: 3 attempts, 10 sec between each attempt
    # can override when called
    @staticmethod
    def get_response(url: str, retries: int = 3, delay: int = 10) -> requests.Response:
        last_exc: Exception | None = None

        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url)
                if response.status_code == 200:
                    return response
                print(
                    f"Attempt {attempt}/{retries} failed for {url} "
                    f"with status {response.status_code}"
                )
            except requests.RequestException as exc:
                last_exc = exc
                print(f"Attempt {attempt}/{retries} raised exception for {url}: {exc}")

            if attempt < retries:
                time.sleep(delay)

        if last_exc:
            raise last_exc
        raise RuntimeError(
            f"Failed to retrieve data from {url} after {retries} attempts"
        )

    @staticmethod
    def get_response_auth(
        url: str, api_key: str, retries: int = 3, delay: int = 10
    ) -> requests.Response:
        last_exc: Exception | None = None

        headers = {"x-auth-token": api_key}

        for attempt in range(1, retries + 1):
            try:
                response = requests.get(url, headers=headers)

                if response.status_code == 200:
                    return response

                print(
                    f"Attempt {attempt}/{retries} failed for {url} "
                    f"with status {response.status_code}"
                )

            except requests.RequestException as exc:
                last_exc = exc
                print(f"Attempt {attempt}/{retries} raised exception for {url}: {exc}")

            if attempt < retries:
                time.sleep(delay)

        if last_exc:
            raise last_exc

        raise RuntimeError(
            f"Failed to retrieve data from {url} after {retries} attempts"
        )

    @staticmethod
    def unmarshal_json(response: requests.Response, struct_type: Type[T]) -> T | None:
        if response.status_code == 200:
            data_json: Any = response.json()
            return struct_type(**data_json)
        return None

    @staticmethod
    def convert_to_df(response: requests.Response) -> pd.DataFrame:
        """Convert List[Any] to pandas dataframe"""
        json_str = response.content.decode("utf-8")
        return pd.DataFrame(json.loads(json_str))
