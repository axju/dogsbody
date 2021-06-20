"""the command line interface"""
from argparse import ArgumentParser
import dogsbody
from .daemon import run_source, load_settings


def main():
    """the cli"""
    parser = ArgumentParser()
    parser.add_argument('--config', help='Set an alternative configuration file.')
    parser.add_argument('-v', '--version', action='version', version=dogsbody.__version__)
    parser.add_argument('-p', '--password', default=None)

    args = parser.parse_args()
    settings = load_settings(args.config)
    if args.password:
        settings['password'] = args.password
    run_source(settings)


if __name__ == '__main__':
    main()
