import os
import sys
from pathlib import Path

from odc_sdk.utils.dataset_endpoints import DatasetClient
from odc_sdk.utils.stats_endpoints import StatsClient


def check_env_file():
    # Make sure the local env file is present in the root directory
    env_path = Path(__file__).resolve().parent / "odc_sdk_generated.env"
    if not env_path.exists():
        print(f"⚠️  Warning: {env_path.name} not found in root.")
        return False
    print(f"✅ Found {env_path.name} file.")
    return True


def run_live_stats():
    print("\n=== 1. Functional Test: StatsClient (Live) ===")
    try:
        stats = StatsClient()
        print("Fetching global stats from SciCrunch...")
        df_datasets = stats.datasets_df()
        print(f"✅ Success! Got {len(df_datasets)} datasets in global stats.")
        print(df_datasets.columns)
        print(df_datasets[['datasetid', 'active']].head(3))  # Quick preview

        # Grab a live ID to chain into the next test
        return df_datasets['datasetid'].iloc[0] if not df_datasets.empty else None
    except Exception as e:
        print(f"❌ Stats endpoint failed: {e}")
        return None


def run_live_dataset(dataset_id):
    print(f"\n=== 2. Functional Test: DatasetClient on ID: {dataset_id} ===")
    try:
        # Client automatically hooks into the local .env key
        client = DatasetClient()

        print(f"Fetching metadata for dataset {dataset_id}...")
        info = client.info(dataset_id)
        print(f"✅ Metadata received! Title: '{info.get('title', 'N/A')}'")

        print(f"Fetching data dictionary for dataset {dataset_id}...")
        df_dict = client.dictionary_df(dataset_id)
        print(f"✅ Data dictionary loaded into DataFrame ({df_dict.shape[1]} columns).")
        print(df_dict.head(2))

        print(f"Downloading actual data matrix for dataset {dataset_id}...")
        df_data = client.data_df(dataset_id)
        print(f"✅ Data downloaded! Matrix shape: {df_data.shape[0]} rows x {df_data.shape[1]} columns.")

    except RuntimeError as re:
        # Catch auth issues (common if the SciCrunch key lacks specific Tier permissions)
        if "401" in str(re) or "403" in str(re):
            print(
                f"❌ Auth Error (401/403): Invalid API key or insufficient permissions for dataset {dataset_id}."
            )
        else:
            print(f"❌ Runtime error: {re}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    print("Starting ODC-TBI SDK functional tests...")
    check_env_file()

    # 1. Fetch public stats and bootstrap a live dataset ID
    sampled_id = run_live_stats()

    # Default fallback using a real hash from your previous log if stats failed
    if not sampled_id:
        sampled_id = "09d23cc78b99e9931be38e9e08ed0a97"
        print(f"Stats unavailable. Using fallback ID: {sampled_id}")

    # 2. Run the authenticated data retrieval test
    run_live_dataset(sampled_id)