from logging import getLogger
from time import sleep

logger = getLogger('dogsbody.runtime')

SOURCE = None
WORKDIR = None
SETTINGS = None


def set_current(source=None, workdir=None, settings=None):
    global SOURCE, WORKDIR, SETTINGS
    if source is not None:
        SOURCE = source
    if workdir is not None:
        WORKDIR = workdir
    if settings is not None:
        SETTINGS = settings


def info():
    logger.info('SOURCE="%s", WORKDIR="%s", SETTINGS="%s"', SOURCE, WORKDIR, SETTINGS)


def delete_source():
    SOURCE.unlink()


def wait_until_source_remove(dt=1):
    while SOURCE and SOURCE.is_file():
        sleep(dt)
