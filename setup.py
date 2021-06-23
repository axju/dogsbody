import os
from pathlib import Path
from setuptools import setup

# allow setup.py to be run from any path
os.chdir(Path(__file__).resolve().parent)

setup(
    packages=['dogsbody'],
    include_package_data=True,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    install_requires=[
        'importlib-metadata; python_version < "3.8.0"',
        'dynaconf',
    ],
    entry_points={
        'console_scripts': [
            'dogsbody=dogsbody.__main__:main',
            'dogsbody-bundle=dogsbody.bundle:cli',
            'dogsbody-daemon=dogsbody.daemon:cli',
        ]
    }
)
