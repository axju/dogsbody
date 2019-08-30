"""A common file for all classes"""
import os
import io
from tempfile import mkdtemp
from base64 import urlsafe_b64encode
from logging import getLogger
from zipfile import ZipFile, ZIP_DEFLATED
from subprocess import call
from shutil import rmtree

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except ImportError:
    logger = getLogger(__name__)
    logger.info('No cryptography. You cannot use the password! '
                'To fix it install "cryptography"')


class Unzipper():
    """
    Manage the data.
    The class can create a data file from a source directory or vice versa.
    """

    def __init__(self, source, password=None):
        """
        - source = data file or source directory
        - password = set password to activate encrypted
        """
        super(Unzipper, self).__init__()
        self.logger = getLogger('Unzipper')
        self.logger.debug('Create Unzipper for source="%s"', source)

        self.source = os.path.abspath(source)
        try:
            self.set_password(password)
        except NameError:
            raise Exception('No cryptography. You cannot use the password! '
                            'To fix it install "cryptography"')

    def set_password(self, password=None):
        """Set a string as the password"""
        self.password = None
        if password:
            self.logger.debug('Activate the encrypten')
            password = password.encode()
            salt = b'O\xe6\x1b\xf5=\xe5\xb2?\xf2\x11\xd4b\xbc\x82@\x05'
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
                backend=default_backend()
            )
            self.password = urlsafe_b64encode(kdf.derive(password))

    def create(self, filename):
        """Create the data file"""
        if not os.path.isdir(self.source):
            raise Exception('"{}" must be a directory!'.format(self.source))

        if os.path.isdir(filename):
            raise Exception('"{}" is a directory!'.format(filename))

        if os.path.isfile(filename):
            self.logger.info('The file "%s" already exist! '
                             'We overrid it :P', filename)

        zip_buffer = io.BytesIO()
        with ZipFile(zip_buffer, "a", ZIP_DEFLATED, False) as zfile:
            for root, _, files in os.walk(self.source):
                for file in files:
                    fname = os.path.join(root, file)
                    fnamer = os.path.relpath(fname, self.source)
                    zfile.write(fname, fnamer)

        if not self.password:
            with open(filename, 'wb') as file:
                file.write(zip_buffer.getvalue())
        else:
            fernet = Fernet(self.password)
            encrypted = fernet.encrypt(zip_buffer.getvalue())

            with open(filename, 'wb') as file:
                file.write(encrypted)

    def unzip(self, directory):
        """Unzip file to source directory."""
        if not os.path.isfile(self.source):
            raise Exception('"{}" must be a file'.format(self.source))

        if not os.path.isdir(directory):
            self.logger.info('Create directory "%s"', directory)
            os.makedirs(directory)
        elif os.listdir(directory):
            raise Exception('"{}" is not empty'.format(directory))

        zip_buffer = io.BytesIO()
        if not self.password:
            with open(self.source, 'rb') as file:
                zip_buffer.write(file.read())
        else:
            with open(self.source, 'rb') as file:
                data = file.read()

            fernet = Fernet(self.password)
            encrypted = fernet.decrypt(data)
            zip_buffer.write(encrypted)

        with ZipFile(zip_buffer) as zfile:
            zfile.extractall(directory)


class Dogsbody():
    """Unzip the data file and execute or create one."""

    def __init__(self, password=None):
        self.logger = getLogger('Dogsbody')
        self.password = password
        self.logger.debug('Create Dogsbody object')

    def create(self, source, filename):
        """Create the data file"""
        self.logger.info('Create file')
        unzipper = Unzipper(source, password=self.password)
        unzipper.create(filename)

    def run(self, source):
        """Unzip the data file and execute"""
        unzipper = Unzipper(source, password=self.password)
        workdir = mkdtemp()
        self.logger.info('Create workdir "%s"', workdir)
        unzipper.unzip(workdir)

        os.chdir(workdir)
        self.logger.info('Change to workdir.')

        if os.path.isfile('main.sh'):
            call(['chmod', 'a+x', 'main.sh'])
            self.logger.info('run the main.sh file ...')
            call(['./main.sh'])
        else:
            self.logger.info('No main.sh file!')

        rmtree(workdir)
        self.logger.info('Delete workdir "%s"', workdir)
