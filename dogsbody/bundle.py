"""the command line interface"""
import os
import io
from logging import getLogger
from base64 import urlsafe_b64encode
from zipfile import ZipFile, ZIP_DEFLATED
from argparse import ArgumentParser

logger = getLogger(__name__)
try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    logger.info('No cryptography. You cannot use the password! '
                'To fix it install "cryptography"')


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


def create_bundle(directory, filename, password=None):
    zip_buffer = io.BytesIO()
    with ZipFile(zip_buffer, 'a', ZIP_DEFLATED, False) as zfile:
        for root, _, files in os.walk(directory):
            for file in files:
                fname = os.path.join(root, file)
                fnamer = os.path.relpath(fname, directory)
                zfile.write(fname, fnamer)

    if not password:
        with open(filename, 'wb') as file:
            file.write(zip_buffer.getvalue())
    else:
        fernet = Fernet(get_password(password))
        encrypted = fernet.encrypt(zip_buffer.getvalue())

        with open(filename, 'wb') as file:
            file.write(encrypted)


def extract_bundle(filename, directory, password=None):
    zip_buffer = io.BytesIO()
    if not password:
        with open(filename, 'rb') as file:
            zip_buffer.write(file.read())
    else:
        with open(filename, 'rb') as file:
            data = file.read()

        fernet = Fernet(get_password(password))
        encrypted = fernet.decrypt(data)
        zip_buffer.write(encrypted)

    with ZipFile(zip_buffer) as zfile:
        zfile.extractall(directory)


def cli():
    parser = ArgumentParser()
    parser.add_argument('-p', '--password', default=None)
    parser.add_argument('-v', '--verbose', action='store_true')
    subparser = parser.add_subparsers(dest='action')

    subparser_create = subparser.add_parser('create')
    subparser_create.add_argument('directory')
    subparser_create.add_argument('filename')

    subparser_extract = subparser.add_parser('extract')
    subparser_extract.add_argument('filename')
    subparser_extract.add_argument('directory')

    args = parser.parse_args()
    if args.action == 'create':
        create_bundle(args.directory, args.filename, args.password)
    else:
        extract_bundle(args.filename, args.directory, args.password)


if __name__ == '__main__':
    cli()
