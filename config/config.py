import os
from typing import Dict, List, Optional

import yaml
from pydantic import BaseModel, BaseSettings

from config.logging import LOGGER
from config.package import CONFIG_PATH


def load_yaml_config():
    with open(CONFIG_PATH, "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as e:
            LOGGER.info(f"Error loading config from {CONFIG_PATH}")


class BookmarkModel(BaseModel):
    config: str


class GCPModel(BaseModel):
    project_id: str
    secrets: Optional[Dict]
    secrets: Optional[List]
    syncbucket: Optional[str]


class SpecModel(BaseModel):
    gcp: Optional[GCPModel] = None
    bookmark: Optional[BookmarkModel] = None


class MetadataModel(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DataProductModel(BaseModel):
    spec: Optional[SpecModel]
    metadata: Optional[MetadataModel]
    version: str


class Settings(BaseSettings):
    dataproduct: DataProductModel
    test_secret: Optional[str]
    vdl_test_secret: Optional[str]

    class Config:
        env_prefix = "VDL_"
        env_nested_delimiter = "__"
        secrets_dir = os.getenv("VDL_DATAPRODUCT_SECRETS_PATH")
        immutable: True


def get_settings() -> Settings:
    settings_yml = load_yaml_config()
    dataproduct = DataProductModel(
        version=settings_yml["version"],
        metadata=settings_yml["metadata"],
        spec=settings_yml["spec"],
    )
    settings = Settings(dataproduct=dataproduct)
    return settings
