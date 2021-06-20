"""Top-level package for dogsbody"""
try:
    from importlib.metadata import version, PackageNotFoundError
except ModuleNotFoundError:
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version('dogsbody')
except PackageNotFoundError:
    __version__ = 'unknown'
finally:
    del version, PackageNotFoundError
