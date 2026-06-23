import pytest
from unittest.mock import MagicMock, patch
import pandas as pd
from odc_sdk.utils.dataset_endpoints import DatasetClient  # Assicurati che il percorso del file sia corretto


# --- FIXTURES FOR MOCKING ---

@pytest.fixture
def mock_api_response():
    """Simula una risposta standard dell'API SciCrunch/ODC"""
    mock = MagicMock()
    mock.status_code = 200
    # Simuliamo un payload tipico JSON inviato dal server
    mock.json.return_value = {
        "status": "success",
        "data": [
            {"subject_id": "SUB_01", "group": "Control", "score": 15.5},
            {"subject_id": "SUB_02", "group": "TBI", "score": 9.2}
        ],
        "variables": [
            {"name": "subject_id", "type": "string"},
            {"name": "score", "type": "float"}
        ],
        "title": "Test TBI Study"
    }
    return mock


# --- UNIT TESTS ---

def test_client_initialization_with_explicit_key():
    """Verifica che il client salvi la chiave passata esplicitamente"""
    client = DatasetClient(api_key="chiave_esplicita_123")
    assert client.api_key == "chiave_esplicita_123"


@patch("odc_sdk.utils.dataset_endpoints.import_api_key")
def test_client_initialization_with_env_fallback(mock_import):
    """Verifica che il client recuperi la chiave dal file .env se non passata"""
    mock_import.return_value = "chiave_dal_file_env"

    client = DatasetClient()

    assert client.api_key == "chiave_dal_file_env"
    mock_import.assert_called_once()


@pytest.mark.parametrize("dataset_id,expected_url", [
    (105, "https://services.scicrunch.io/odc/dataset/105"),
    ("ODC-TBI-001", "https://services.scicrunch.io/odc/dataset/ODC-TBI-001")
])
def test_url_composition_without_trailing_slashes(dataset_id, expected_url):
    """Verifica che gli URL vengano composti correttamente sia con ID numerici che stringhe"""
    client = DatasetClient(api_key="mock_key")
    assert client._base_url_for(dataset_id) == expected_url


def test_info_method_parsing(mock_api_response):
    """Verifica che il metodo info() intercetti l'URL corretto e restituisca il JSON"""
    client = DatasetClient(api_key="mock_key")
    # Sostituiamo il metodo di rete reale con il nostro mock
    client._auth_get = MagicMock(return_value=mock_api_response)

    result = client.info(42)

    # Controlliamo che abbia chiamato l'URL corretto (senza slash finale!)
    client._auth_get.assert_called_once_with("https://services.scicrunch.io/odc/dataset/42/info", "mock_key")
    assert result["title"] == "Test TBI Study"


def test_pandas_dataframe_data_export(mock_api_response):
    """Verifica che data_df() converta correttamente i dati grezzi in un DataFrame Pandas valido"""
    client = DatasetClient(api_key="mock_key")
    client._auth_get = MagicMock(return_value=mock_api_response)

    df = client.data_df(42)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 3)  # 2 righe, 3 colonne
    assert list(df.columns) == ["subject_id", "group", "score"]
    assert df.loc[0, "subject_id"] == "SUB_01"


def test_pandas_dataframe_dictionary_export(mock_api_response):
    """Verifica che dictionary_df() estragga la sotto-chiave 'variables' nel DataFrame"""
    client = DatasetClient(api_key="mock_key")
    client._auth_get = MagicMock(return_value=mock_api_response)

    df = client.dictionary_df(42)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
    assert "name" in df.columns