from dataclasses import dataclass


# swagger shows id, actual response is datasetid?
@dataclass
class DatasetStat:
    datasetid: str
    lab_status: str
    timestamp: int
    last_updated_time: int
    last_uploaded_time: int
    active: int
    field_count: int
    record_count: int
    labid: str
    community: str


@dataclass
class UserLab:
    labid: str
    community: str


# guid, created in swagger, not in actual response
# swagger shows id, actual response is userid?
@dataclass
class UserStat:
    userid: str
    timestamp: str
    labs: str  # was List[UserLab] before, left for user to parse


@dataclass
class LabStat:
    labid: str
    community: str
    timestamp: int
    name: str
    cid: int
    curated: str


# NOTE: different from swagger
@dataclass
class DownloadStat:
    entity_id: str
    shortName: str
    name: str
    download_count: int
    lab_name: str
