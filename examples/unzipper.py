import os
import logging
from dogsbody.cls import Unzipper

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)

source = os.path.join(os.path.dirname(__file__), 'data', 'source')
output = os.path.join(os.path.dirname(__file__), 'data', 'output')
filename = os.path.join(os.path.dirname(__file__), 'data', 'test.zip')

# create file
unzipper = Unzipper(source)
unzipper.create(filename)

# unzip file
unzipper = Unzipper(filename)
unzipper.unzip(output)


# create file
#unzipper = Unzipper(source, password='1234')
#unzipper.create(filename)

# unzip file
#unzipper = Unzipper(filename, password='1234')
#unzipper.unzip(output)
