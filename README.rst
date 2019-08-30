========
Dogsbody
========
A tool to create and execute a "special setup"/"data file".

Install
-------
::

  pip install dogsbody

How to use
----------
The "special setup" is a directory with at least one file. The main.sh file is
executed and run your custom commands. To pass the directory, it is compressed
into a file. You can also add other stuff to the source directory.

Encryption
----------
To use the encryption (the -p option) you have to install "cryptography".::

  pip install cryptography

Commands
--------
Some information::

  dogsbody --help

Create the "data file"/"special setup"::

  dogsbody create source filename

Executed the "special setup"::

  dogsbody run source

And now both with activated encryption::

  dogsbody -p "1234" create source filename
  dogsbody -p "1234" run source

Why?
----
I need to setup a project on a raspberry pi. It should be a single file
including everything.

Development
-----------
Some information for crazy developers. Virtual environment windows::

  python -m venv venv
  venv\Scripts\activate

Virtual environment linux::

  python3 -m venv venv
  source venv/bin/activate

Setup project::

  python -m pip install --upgrade pip wheel setuptools twine tox flake8 pylint pylama
  pip install -e .

Run some test::

  tox

Create package::

  python setup.py sdist bdist_wheel

Upload package::

  twine upload dist/*

Run it on Termux::

  pkg install clang # for cryptography
  ./dev.sh
