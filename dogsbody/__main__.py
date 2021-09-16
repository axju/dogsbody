"""the command line interface"""
from argparse import ArgumentParser
from dogsbody import __version__
from .dog import dogsbody
from .utils import load_settings, setup_logger


def main():
    """the cli"""
    parser = ArgumentParser()
    parser.add_argument('-V', '--version', action='version', version=__version__)
    parser.add_argument('-c', '--config', help='Set an alternative configuration file.')
    parser.add_argument('-v', '--verbose', action="count", help="verbose level... repeat up to three times.")
    parser.add_argument('-p', '--password', default=None)
    parser.add_argument('path', default=None)

    args = parser.parse_args()
    setup_logger(args.verbose)
    settings = load_settings(args.config, password=args.password)
    dogsbody(args.path, **settings)


if __name__ == '__main__':
    main()
