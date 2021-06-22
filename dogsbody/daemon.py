"""the command line interface"""
from time import sleep
from argparse import ArgumentParser
from pathlib import Path
from logging import getLogger
from tempfile import mkdtemp
from shutil import rmtree
from subprocess import call

from .bundle import extract_bundle
from .runtime import set_current
from .utils import setup_logger, load_settings


logger = getLogger('dogsbody.daemon')


def iter_source(settings):
    for path in settings.get('source', []):
        filename = Path(path).resolve()
        if filename.is_file():
            yield filename


def execute(path):
    logger.info('Change to workdir.')

    if Path(path / 'main.py').is_file():
        exec(Path(path / 'main.py').read_text())
        logger.info('run the main.py file ...')

    elif Path(path / 'main.sh').is_file():
        filename = str(Path(path / 'main.sh'))
        call(['chmod', 'a+x', filename])
        call([filename])
        logger.info('run the main.sh file ...')

    else:
        logger.info('No main.sh file!')
        return False
    return True


def dogsbody(settings):
    for path in iter_source(settings):
        workdir = Path(mkdtemp())
        set_current(path, workdir, settings)
        logger.info('Create workdir "%s"', workdir)

        extract_bundle(path, workdir, settings.get('password'))
        logger.info('extract bundle')

        execute(workdir)
        logger.info('execute bundle')

        rmtree(workdir)
        logger.info('Delete workdir "%s"', workdir)


def main(settings, loop=True):
    interval = settings.get('interval', 10)
    logger.info('Run daemon with interval=%i', interval)

    error_counter = 0
    while loop:
        try:
            dogsbody(settings)
            for _ in range(interval):
                sleep(1)
            error_counter = 0

        except KeyboardInterrupt:
            break

        except Exception:
            error_counter += 1
            logger.error('fatal error in loop', exc_info=True)
            if error_counter > 5:
                break


def cli():
    """the cli"""
    parser = ArgumentParser()
    parser.add_argument('--config', help='Set an alternative configuration file.')
    parser.add_argument('-v', '--verbose', action="count", help="verbose level... repeat up to three times.")
    parser.add_argument('-p', '--password', default=None)

    args = parser.parse_args()
    setup_logger(args.verbose)
    settings = load_settings(args.config, password=args.password)
    main(settings)


if __name__ == '__main__':
    cli()
