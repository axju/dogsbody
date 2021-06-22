import logging

from dynaconf import Dynaconf


logger = logging.getLogger('dogsbody.utils')


DEFAULT_SETTING_FILES = ['settings.toml']


def load_settings(filename=None, **kwargs):
    settings_files = [filename] if filename is not None else []
    settings_files = settings_files + DEFAULT_SETTING_FILES
    settings = Dynaconf(settings_files=settings_files)
    settings.update(kwargs)
    return settings


def setup_logger(level=0, root=''):
    """setup the root logger"""
    local_logger = logging.getLogger(root)
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, level or 0)]
    local_logger.setLevel(level)
    ch = logging.StreamHandler()
    ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    local_logger.addHandler(ch)
