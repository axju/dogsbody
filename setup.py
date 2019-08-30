import os
from setuptools import find_packages, setup

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()

setup(
    name='dogsbody',
    version='0.0.1',
    description='A tool to create and execute a "special setup"/"data file".',
    long_description=README,
    url='???',
    author='Axel Juraske',
    author_email='axel.juraske@short-report.de',
    license='MIT',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    entry_points = {
        'console_scripts': [
            'dogsbody=dogsbody.cli:main',
        ]
    }
)
