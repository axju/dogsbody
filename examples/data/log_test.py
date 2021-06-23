from dogsbody import runtime
from dogsbody.utils import setup_logger

logger = setup_logger(3, filename=runtime.SOURCE.parent / 'log.txt')

logger.debug('test debug')
logger.info('test info')

runtime.info()
runtime.delete_source()
