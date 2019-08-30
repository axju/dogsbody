"""the command line interface"""
import os
import logging
from argparse import ArgumentParser
from dogsbody.cls import Dogsbody


def main():
    """the cli"""
    parser = ArgumentParser()
    parser.add_argument('-p', '--password', default=None)
    parser.add_argument('-v', '--verbose', action='store_true')
    subparser = parser.add_subparsers(dest='cmd')

    parser_run = subparser.add_parser('run')
    parser_run.add_argument('source')

    parser_create = subparser.add_parser('create')
    parser_create.add_argument('source')
    parser_create.add_argument('filename')

    args = parser.parse_args()

    level = logging.INFO
    if args.verbose:
        level = logging.DEBUG
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=level, format=log_format)

    dogsbody = Dogsbody(password=args.password)
    if args.cmd == 'run':
        if os.path.isfile(args.source):
            dogsbody.run(args.source)
        else:
            print(f'{args.source} is no file')

    elif args.cmd == 'create':
        dogsbody.create(args.source, args.filename)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
