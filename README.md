# ODC SDK, Python version

Software Development Kit (SDK) to work with ODC platform. https://services.scicrunch.io/odc/docs

For optimal support, I recommend using latest Python versions (3.13.x or 3.14.x at the time of writing). Prior Python versions should work but not guaranteed. See `requirements.txt` file for all required dependencies.

Note: package name is `odc_sdk`

## Repo overview

- odc_sdk: This is source code for odc_sdk python package you will be installing.
  - configs: Setup .env file to store ODC API token. Functions will read from .env file when necessary.
  - models: Schema used when marshal response json easier to work with data format.
  - client.py: Functions user will interact with the most
  - endpoints.py: Helper functions to create full endpoint
  - request_handler.py: Http requests and middleware
- dist: Store latest pre-built wheel and tar.gz files. `pip install git+` command looks into this folder first on install. Skips build step if these files are present.
- docs: Documentation, examples, decisions made during design process.
- tests: Use pytest to run.

## Install

Production

```shell
python3 -m pip install git+https://github.com/ucsf-ferguson-lab/odc_python_sdk
```

Note: Unix systems might require `--break-system-packages` flag

```shell
python3 -m pip install git+https://github.com/ucsf-ferguson-lab/odc_python_sdk --break-system-packages
```

Dev

```shell
python3 -m pip install git+https://github.com/ucsf-ferguson-lab/odc_python_sdk.git@dev
```

### Dependencies (not required)

If you need to install the required dependencies. Run

```shell
python3 -m pip install -r requirements.txt
```

### Virtual environment (not required)

See https://docs.python.org/3/library/venv.html to setup virtualenv. Follow above steps to install package inside virtualenv.

### Uninstall

```shell
python3 -m pip uninstall odc_sdk
```

## Quick start

See code examples in `/docs`. Code below copied from `/docs/stats/example.py`.

```python
from odc_sdk.endpoints import StatEndpoints
from odc_sdk.client import StatsClient
from odc_sdk.models import stats_responses as stats_models

if __name__ == "__main__":
    stat_endpoints = StatEndpoints.from_base_url()
    stat_client = StatsClient(stat_endpoints)

    # available methods: user_stats, download_stats, lab_stats, dataset_stats
    user_stats = stat_client.user_stats(stats_models)

    print(user_stats)
```

### Supported routes

See https://services.scicrunch.io/odc/docs for full swagger documentation

public stats endpoints (no auth required)

- GET /stats/datasets
- GET /stats/users
- GET /stats/labs
- GET /stats/downloads
