import os
from dotenv import load_dotenv, set_key
from pathlib import Path

BASE_URL = "https://services.scicrunch.io/odc"

# dynamically find the root --> "odc_sdk_generated.env"
CURRENT_FILE_DIR = Path(__file__).resolve().parent.parent # --> this aims to the root
PROJECT_ROOT = CURRENT_FILE_DIR.parent

FILENAME = "odc_sdk_generated.env"
DEFAULT_ENV_PATH = PROJECT_ROOT / FILENAME

# read from .env file, use init_api_key() to setup .env file
# don't pass any args if .env file created with init_api_key()
def import_api_key(
    key_name: str = "ODC_API_KEY", dotenv_path: str = DEFAULT_ENV_PATH
) -> str:
    load_dotenv(dotenv_path)
    api_key: str | None = os.getenv(key_name)

    if api_key and api_key != "":
        return api_key
    else:
        raise ValueError("Unable to import API key from {dotenv_path}")


# don't need to check if api key invalid, invalid api key can't access authenticated routes
def init_api_key(dotenv_path: Path = DEFAULT_ENV_PATH) -> None:
    print("Enter API key:")
    api_key: str | None = input()

    if api_key and api_key != "":
        # os agnostic, creates in root
        dotenv_path.touch(mode=0o600, exist_ok=True)  # create file if DNE, overrides

        set_key(
            dotenv_path=dotenv_path, key_to_set="ODC_API_KEY", value_to_set=api_key
        )
        print(f"Env file created at {dotenv_path}")
    else:
        raise ValueError("Empty API key is not allowed")
