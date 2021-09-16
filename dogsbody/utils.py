import logging
from pathlib import Path
from subprocess import call
from dynaconf import Dynaconf


logger = logging.getLogger(__name__)


DEFAULT_SETTING_FILES = ['/etc/dogsbody.toml', 'settings.toml']


def load_settings(filename=None, **kwargs):
    settings_files = [filename] if filename is not None else []
    settings_files = settings_files + DEFAULT_SETTING_FILES
    settings = Dynaconf(settings_files=settings_files)
    settings.update(kwargs)
    return settings


def setup_logger(level=0, filename=None, root='', format_str='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    """setup the root logger"""
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    level = levels[min(len(levels) - 1, level or 0)]
    local_logger = logging.getLogger(root)
    local_logger.setLevel(level)
    if filename is None:
        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter(format_str))
        ch.setLevel(level)
        local_logger.addHandler(ch)
    else:
        fh = logging.FileHandler(filename)
        fh.setFormatter(logging.Formatter(format_str))
        fh.setLevel(level)
        local_logger.addHandler(fh)
    return local_logger


def execute(path):
    logger.info('Change to workdir.')

    if Path(path / 'main.py').is_file():
        try:
            exec(Path(path / 'main.py').read_text(encoding='UTF-8'), globals())
            logger.info('run the main.py file ...')
        except Exception as e:
            logger.warning('error in main.py "%s"', str(e))

    elif Path(path / 'main.sh').is_file():
        filename = str(Path(path / 'main.sh'))
        call(['chmod', 'a+x', filename])
        call([filename])
        logger.info('run the main.sh file ...')

    else:
        logger.info('No main.sh file!')
        return False
    return True
