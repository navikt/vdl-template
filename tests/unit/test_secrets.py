import json
import logging
import os
from pathlib import Path
from unittest import mock

import pytest

import config.secrets as secrets
from config.config import get_settings

logger = logging.getLogger(__name__)


@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(
        os.environ,
        {"VDL_DATAPRODUCT_SECRETS_PATH": str(Path.cwd() / "tests/data/vault")},
    ):
        yield


def test_single_env():
    logger.info(f'secrets path: {os.getenv("VDL_DATAPRODUCT_SECRETS_PATH")}')
    secrets.set_env_variables_from_secrets(get_settings())
    assert os.getenv("TEST_SECRET") == "123"


def test_single_json_env():
    logger.info(f'secrets path: {os.getenv("VDL_DATAPRODUCT_SECRETS_PATH")}')
    secrets.set_env_variables_from_secrets(get_settings())
    with open(os.getenv("TEST_SECRET_JSON")) as f:
        secret_json = json.load(f)
        assert secret_json["secret"] == "123"
