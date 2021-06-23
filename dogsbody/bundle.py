"""the command line interface"""
from io import BytesIO
from logging import getLogger
from base64 import urlsafe_b64encode
from zipfile import ZipFile, ZIP_DEFLATED
from argparse import ArgumentParser
from pathlib import Path

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from .utils import setup_logger


logger = getLogger('dogsbody.bundle')


def get_password(password, salt=None):
    """get a string as the password"""
    logger.debug('Activate the encrypten')
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt or b'O\xe6\x1b\xf5=\xe5\xb2?\xf2\x11\xd4b\xbc\x82@\x05',
        iterations=100000,
        backend=default_backend()
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))


def create_bundle(path, filename, password=None):
    source = Path(path)
    zip_buffer = BytesIO()
    with ZipFile(zip_buffer, 'a', ZIP_DEFLATED, False) as zfile:
        if source.is_file():
            if source.suffix == '.py':
                zfile.write(source, 'main.py')
            else:
                zfile.write(source, source.name)
        for file in source.glob('**/*'):
            zfile.write(file, file.relative_to(source))

    if not password:
        with open(filename, 'wb') as file:
            file.write(zip_buffer.getvalue())
    else:
        fernet = Fernet(get_password(password))
        encrypted = fernet.encrypt(zip_buffer.getvalue())

        with open(filename, 'wb') as file:
            file.write(encrypted)
    return True


def extract_bundle(filename, directory, password=None):
    zip_buffer = BytesIO()
    if not password:
        with open(filename, 'rb') as file:
            zip_buffer.write(file.read())
    else:
        with open(filename, 'rb') as file:
            data = file.read()

        fernet = Fernet(get_password(password))
        try:
            encrypted = fernet.decrypt(data)
        except InvalidToken:
            logger.warning('Wrong password')
            return False

        zip_buffer.write(encrypted)

    with ZipFile(zip_buffer) as zfile:
        zfile.extractall(directory)
    return True


def cli():
    parser = ArgumentParser()
    parser.add_argument('-p', '--password', default=None)
    parser.add_argument('-v', '--verbose', action="count", help="verbose level... repeat up to three times.")
    subparser = parser.add_subparsers(dest='action')

    subparser_create = subparser.add_parser('create')
    subparser_create.add_argument('directory')
    subparser_create.add_argument('filename')

    subparser_extract = subparser.add_parser('extract')
    subparser_extract.add_argument('filename')
    subparser_extract.add_argument('directory')

    args = parser.parse_args()
    setup_logger(args.verbose)
    if args.action == 'create':
        create_bundle(args.directory, args.filename, args.password)
    else:
        extract_bundle(args.filename, args.directory, args.password)


if __name__ == '__main__':
    cli()
