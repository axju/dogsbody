"""the command line interface"""
from time import sleep
from argparse import ArgumentParser
from pathlib import Path
from logging import getLogger

from .dog import dogsbody
from .utils import setup_logger, load_settings


logger = getLogger('dogsbody.daemon')


def iter_source(settings):
    files = []
    for path in settings.get('files', []):
        filename = Path(path).resolve()
        if filename.is_file():
            files.append(filename)

    for root in settings.get('media_root', []):
        for device in Path(root).iterdir():
            if not device.is_dir():
                continue
            for path in settings.get('portable', []):
                filename = Path(device / path).resolve()
                if filename.is_file():
                    files.append(filename)

    if settings.get('only_first', False) and len(files) > 0:
        return [files[0]]
    return files


def main(settings, loop=True):
    interval = settings.get('interval', 10)
    run_only_once = settings.get('run_only_once', True)
    logger.info('Run daemon with interval=%i', interval)

    error_counter = 0
    run_it = True if settings.get('run_on_startup', True) else len(list(iter_source(settings))) == 0
    while loop:
        try:
            if run_it or not run_only_once:
                dogsbody(settings)
            run_it = len(list(iter_source(settings))) == 0

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
