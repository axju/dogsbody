"""the command line interface"""
import os
from time import sleep
from logging import getLogger
from argparse import ArgumentParser
from tempfile import mkdtemp
from subprocess import call
from shutil import rmtree

from dynaconf import Dynaconf

from .bundle import extract_bundle


logger = getLogger(__name__)


def runner_main(source, settings):
    os.chdir(source)
    logger.info('Change to workdir.')

    if os.path.isfile('main.sh'):
        call(['chmod', 'a+x', 'main.sh'])
        logger.info('run the main.sh file ...')
        call(['./main.sh'])
    else:
        logger.info('No main.sh file!')
    return True


def get_source(settings):
    yield 'test'


def get_runner(settings):
    return runner_main


def run_source(settings):
    for source in get_source(settings):
        workdir = mkdtemp()
        logger.info('Create workdir "%s"', workdir)
        extract_bundle(source, workdir, settings.get('password'))
        runner = get_runner(settings)
        runner(workdir, settings)
        rmtree(workdir)
        logger.info('Delete workdir "%s"', workdir)


def run(settings):
    print('interval', settings.get('interval'))
    interval = settings.get('interval', 10)

    error_counter = 0
    while True:
        try:
            run_source(settings)
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


def load_settings(filename=None):
    settings_files = [filename] if filename is not None else []
    settings_files = settings_files + ['settings.toml']
    settings = Dynaconf(settings_files=settings_files)
    return settings


def cli():
    """the cli"""
    parser = ArgumentParser()
    parser.add_argument('--config', help='Set an alternative configuration file.')
    parser.add_argument('-p', '--password', default=None)

    args = parser.parse_args()
    settings = load_settings(args.config)
    if args.password:
        settings['password'] = args.password
    run(settings)


if __name__ == '__main__':
    cli()
