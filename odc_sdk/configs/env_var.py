import os
from dotenv import load_dotenv, set_key
from pathlib import Path

BASE_URL = "https://services.scicrunch.io/odc"


# read from .env file, use init_api_key() to setup .env file
# don't pass any args if .env file created with init_api_key()
def import_api_key(
    key_name: str = "ODC_API_KEY", dotenv_filename: str = "odc_sdk_generated.env"
) -> str:
    load_dotenv(dotenv_filename)
    api_key: str | None = os.getenv(key_name)

    if api_key and api_key != "":
        return api_key
    else:
        raise ValueError("Unable to import API key")


# don't need to check if api key invalid, invalid api key can't access authenticated routes
def init_api_key() -> None:
    print("Enter API key:")
    api_key: str | None = input()

    if api_key and api_key != "":
        # os agnostic, creates in current directory
        full_path: str = os.path.join(os.getcwd(), "odc_sdk_generated.env")
        env_file_path: Path = Path(full_path)
        env_file_path.touch(mode=0o600, exist_ok=True)  # create file if DNE, overrides

        set_key(
            dotenv_path=env_file_path, key_to_set="ODC_API_KEY", value_to_set=api_key
        )
        print(f"Env file created at {full_path}")
    else:
        raise ValueError("Empty API key is not allowed")
