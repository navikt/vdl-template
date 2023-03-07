import logging
import os
from pathlib import Path

import coloredlogs
import yaml

# TODO
# from common import database

LOGGER = logging.getLogger("dataprodukt")


def setup_logging(
    default_path=str(Path(__file__).parent / "logging.yml"),
    default_level=logging.INFO,
    env_key="DATAPRODUCT_LOGGING_SETTINGS_PATH",
):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, "rt") as f:
            try:
                config = yaml.safe_load(f.read())
                logging.config.dictConfig(config)
                coloredlogs.install()
            except Exception:
                logging.basicConfig(level=default_level)
                coloredlogs.install(level=default_level)
    else:
        logging.basicConfig(level=default_level)
        coloredlogs.install(level=default_level)


class SnowflakeHandler(logging.Handler):
    """
    A class which sends log records to Snowflake
    """

    def __init__(self, capacity=1):
        """
        Initialize the handler
        """
        logging.Handler.__init__(self)
        self.capacity = capacity
        self.buffer = []
        # self.connection = open_snowflake_connection()

    def shouldFlush(self, record):
        return len(self.buffer) >= self.capacity

    def emit(self, record):
        self.buffer.append(record)
        if self.shouldFlush(record):
            self.flush()

    def flush(self):
        """
        Process records and flush buffer
        """
        self.acquire()
        try:
            self.commit()
            self.buffer.clear()
        finally:
            self.release()

    def close(self):
        try:
            self.flush()
        finally:
            logging.Handler.close(self)

    def json(self, record):
        return record.__dict__

    def commit(self):
        """
        Send the records to Snowflake
        """
        for record in self.buffer:
            try:
                # TODO: Send to SF
                print("Snowflakehandler", self.json(record))

            except Exception:
                self.handleError(record)
