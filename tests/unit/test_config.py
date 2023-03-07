import contextlib
import logging
import os
from pathlib import Path
from unittest import mock

import pytest

import config.config as config
from config.config import get_settings

logger = logging.getLogger(__name__)


@contextlib.contextmanager
def override_settings(**overrides):
    settings = get_settings().Config
    original = {}

    try:
        for key, value in overrides.items():
            original[key] = getattr(settings, key)
            setattr(settings, key, value)

        yield
    finally:
        for key, value in original.items():
            setattr(settings, key, value)


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ,
        {"VDL_DATAPRODUCT_SECRETS_PATH": str(Path.cwd() / "tests/data/vault")},
    ):
        yield


@override_settings(secrets_dir=str(Path.cwd() / "tests/data/vault"))
def test_override_settings_decorator():
    settings = config.get_settings()
    logger.info(f"settings secrets dir {settings.Config.secrets_dir}")
    assert settings.Config.secrets_dir == str(Path.cwd() / "tests/data/vault")


@override_settings(secrets_dir=str(Path.cwd() / "tests/data/vault"))
def test_config_spec():
    conf = get_settings()
    logger.info(conf.dict())
    assert type(conf.dataproduct) == config.DataProductModel


if __name__ == "__main__":
    current_value = os.environ.get("VDL_DATAPRODUCT_SECRETS_PATH")
    os.environ["VDL_DATAPRODUCT_SECRETS_PATH"] = str(Path.cwd() / "tests/data/vault")
    os.environ[
        "VDL_BOOKMARK_CONNECTION"
    ] = f"snowflake://{os.getenv('VDL_BOOKMARK_USR')}:{os.getenv('VDL_BOOKMARK_PWD')}@{os.getenv('VDL_BOOKMARK_ACCOUNT')}/"
    test_config_spec()
    if current_value is not None:
        os.environ["VDL_DATAPRODUCT_SECRETS_PATH"] = current_value
