from logging import getLogger
from argparse import ArgumentParser
from pathlib import Path
from tempfile import mkdtemp
from shutil import rmtree

from .bundle import extract_bundle
from .runtime import set_current
from .utils import execute, setup_logger


logger = getLogger('dogsbody.dog')


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


def execute_file(path, password=None, delete=False):
    try:
        dogsbody(path, password=password)
    except Exception as e:
        logger.error(e)
    if delete:
        path.unlink(missing_ok=True)


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--password', default=None)
    parser.add_argument('-v', '--verbose', action='count', help="verbose level... repeat up to three times")
    parser.add_argument('-d', '--delete', action='store_true', help="delete file, if done")
    parser.add_argument('path', nargs='?', const='.', default='.', help="path to dog file")

    args = parser.parse_args()
    setup_logger(args.verbose)
    path = Path(args.path).resolve()
    logger.info('execute dogsbody with path %s', path)
    if path.is_dir():
        for file in path.iterdir():
            if file.suffix == '.dog':
                execute_file(file, args.password, args.delete)
    elif path.is_file():
        execute_file(file, args.password, args.delete)
    else:
        logger.warning('bad path "%s"', path)


if __name__ == '__main__':
    main()
