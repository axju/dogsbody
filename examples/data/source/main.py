from dogsbody import runtime
from dogsbody.utils import setup_logger

setup_logger(runtime.SOURCE.parent / 'log.txt')

runtime.info()
runtime.delete_source()
