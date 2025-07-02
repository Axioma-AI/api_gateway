import logging
import coloredlogs
import os


def setup_logger(name: str, level: int = logging.INFO, log_file: str = 'app.log') -> logging.Logger:
    """Configure and return a logger with console and file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not os.path.exists('logs'):
        os.makedirs('logs')

    file_handler = logging.FileHandler(os.path.join('logs', log_file), encoding='utf-8')
    file_handler.setLevel(level)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = coloredlogs.ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
