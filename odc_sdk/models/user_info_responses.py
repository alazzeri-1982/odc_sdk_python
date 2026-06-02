from dataclasses import dataclass
from typing import Optional, List


@dataclass
class DatasetFieldTemplate:
    id: int
    uid: int
    timestamp: int
    labid: int
    name: str
    active: bool
    parent_id: int
    submitted: bool
    dataset_names: List[dict]


@dataclass
class Dataset:
    id: int
    uid: int
    name: str
    long_name: str
    description: str
    publications: str
    timestamp: int
    dataset_fields_template_id: int
    lab_status: str
    editor_status: Optional[str]
    curation_status: Optional[str]
    record_count: int
    active: bool
    last_updated_time: int
    last_uploaded_time: int
    template: DatasetFieldTemplate


@dataclass
class Lab:
    id: int
    cid: int
    name: str


@dataclass
class Community:
    id: int
    uid: int
    name: str
    cid: int
    level: int
    date: int


@dataclass
class UserInfo:
    id: int
    guid: int
    email: str
    first_name: str
    middle_initial: Optional[str]
    last_name: str
    organization: str
    datasets: List[Dataset]
    communities: List[Community]
    labs: List[Lab]

    @classmethod
    def from_dict(cls, data: dict) -> "UserInfo":
        return cls(
            id=data["id"],
            guid=data["guid"],
            email=data["email"],
            first_name=data["firstName"],
            middle_initial=data.get("middleInitial"),
            last_name=data["lastName"],
            organization=data["organization"],
            datasets=[cls._parse_dataset(d) for d in data["datasets"]],
            communities=[cls._parse_community(c) for c in data["communities"]],
            labs=[cls._parse_lab(lab) for lab in data["labs"]],
        )

    @staticmethod
    def _parse_dataset(data: dict) -> Dataset:
        return Dataset(
            id=data["id"],
            uid=data["uid"],
            name=data["name"],
            long_name=data["long_name"],
            description=data["description"],
            publications=data["publications"],
            timestamp=data["timestamp"],
            dataset_fields_template_id=data["dataset_fields_template_id"],
            lab_status=data["lab_status"],
            editor_status=data.get("editor_status"),
            curation_status=data.get("curation_status"),
            record_count=data["record_count"],
            active=data["active"],
            last_updated_time=data["last_updated_time"],
            last_uploaded_time=data["last_uploaded_time"],
            template=DatasetFieldTemplate(
                id=data["template"]["id"],
                uid=data["template"]["uid"],
                timestamp=data["template"]["timestamp"],
                labid=data["template"]["labid"],
                name=data["template"]["name"],
                active=data["template"]["active"],
                parent_id=data["template"]["parent_id"],
                submitted=data["template"]["submitted"],
                dataset_names=data["template"]["dataset_names"],
            ),
        )

    @staticmethod
    def _parse_community(data: dict) -> Community:
        return Community(
            id=data["id"],
            uid=data["uid"],
            name=data["name"],
            cid=data["cid"],
            level=data["level"],
            date=data["date"],
        )

    @staticmethod
    def _parse_lab(data: dict) -> Lab:
        return Lab(id=data["id"], cid=data["cid"], name=data["name"])
