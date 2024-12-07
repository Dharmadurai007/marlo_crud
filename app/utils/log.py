import os
import logging
from pathlib import Path, PurePath
from logging.handlers import RotatingFileHandler
from flask.logging import default_handler
from flask import Flask
from typing import Tuple
from config import ProdConfig, DevConfig


def init_logger(app: Flask) -> logging.RootLogger:
    """
    Initialize the logger configs.

    Args:
        app (Flask): Flask app

    Returns:
        logging.RootLogger: Configured logger.
    """
    app.logger.removeHandler(default_handler)
    FORMATTER = logging.Formatter(
        "%(asctime)s — %(name)s — %(levelname)s —  %(filename)s — %(message)s"
    )
    log_path, logger_level, max_bytes, backup_count = _logger_config("root")
    if not Path(log_path).exists():
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(_get_logger_level(logger_level))
    file_handler = RotatingFileHandler(
        log_path, mode="a", maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setFormatter(FORMATTER)
    app.logger.addHandler(file_handler)
    return logger


def _get_logger_level(level: str) -> int:
    """
    Convert string to logging levels

    Args:
        level (str): Log level

    Returns:
        int: logging level
    """
    switcher = {
        "CRITICAL": logging.CRITICAL,
        "FATAL": logging.CRITICAL,
        "ERROR": logging.ERROR,
        "WARNING": logging.WARNING,
        "WARN": logging.WARNING,
        "INFO": logging.INFO,
        "DEBUG": logging.DEBUG,
    }
    return switcher.get(level, logging.NOTSET)


def _get_filename(object, service):
    if service == "root":
        file_name = object.FILE_NAME
    else:
        file_name = object.WORKERS_FILE_NAME
    return file_name


def _logger_config(root_or_worker) -> Tuple[PurePath, str, int, int]:
    """
    Gets the logger configuration from config

    Returns:
        Tuple[PurePath, str, int, int]: Returns log file path, level, maximum words and backup file count.
    """
    config = os.getenv("FLASK_ENV", "DevConfig")
    ROOT_DIR = Path().absolute()
    if config == "DevConfig":
        config_path = DevConfig.LOG_PATH
        file_name = _get_filename(DevConfig, root_or_worker)
        logger_level_config = DevConfig.LOGGER_LEVEL
        max_bytes = DevConfig.MAX_BYTES
        backup_count = DevConfig.BACKUP_COUNT
        if not (
            config_path
            and file_name
            and logger_level_config
            and max_bytes
            and backup_count
        ):
            raise ValueError(6003)
        log_path = PurePath(ROOT_DIR, config_path, file_name)
        logger_level = logger_level_config.upper()
    else:
        config_path = ProdConfig.LOG_PATH
        file_name = _get_filename(ProdConfig, root_or_worker)
        logger_level_config = ProdConfig.LOGGER_LEVEL
        max_bytes = ProdConfig.MAX_BYTES
        backup_count = ProdConfig.BACKUP_COUNT
        if not (
            config_path
            and file_name
            and logger_level_config
            and max_bytes
            and backup_count
        ):
            raise ValueError(6003)
        log_path = PurePath(ROOT_DIR, config_path, file_name)
        logger_level = logger_level_config.upper()
    return log_path, logger_level, max_bytes, backup_count



