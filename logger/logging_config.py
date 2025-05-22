import logging
from colorama import Fore, Style

class ColorFormatter(logging.Formatter):
    """Custom formatter to add colors to log levels"""

    FORMATS = {
        logging.DEBUG: Fore.CYAN + "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s" + Style.RESET_ALL,
        logging.INFO: Fore.GREEN + "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s" + Style.RESET_ALL,
        logging.WARNING: Fore.YELLOW + "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s" + Style.RESET_ALL,
        logging.ERROR: Fore.RED + "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s" + Style.RESET_ALL,
        logging.CRITICAL: Fore.RED + Style.BRIGHT + "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s" + Style.RESET_ALL,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logger(name=None, level=logging.INFO, log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if logger.hasHandlers():
        logger.handlers.clear()

    ch = logging.StreamHandler()
    ch.setFormatter(ColorFormatter())
    logger.addHandler(ch)

    if log_file:
        fh = logging.FileHandler(log_file)
        file_fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
                                     datefmt="%Y-%m-%d %H:%M:%S")
        fh.setFormatter(file_fmt)
        logger.addHandler(fh)

    return logger