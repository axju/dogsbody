import logging
from pathlib import Path
from tempfile import mkdtemp
from shutil import rmtree

from .bundle import extract_bundle
from .runtime import set_current
from .utils import execute


logger = logging.getLogger(__name__)


def dogsbody(path, **settings):
    path = Path(path).resolve()
    workdir = Path(mkdtemp())
    set_current(path, workdir, settings)
    logger.info('Create workdir "%s"', workdir)

    extract_bundle(path, workdir, settings.get('password'))
    logger.info('extract bundle')

    execute(workdir)
    logger.info('execute bundle')

    rmtree(workdir)
    logger.info('Delete workdir "%s"', workdir)
