import os
import codecs

from distutils.core import setup

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            # __version__ = "0.9"
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='maylibre',
    version=get_version('LO_extension/Scripts/python/maylibre.py'),
    packages=[''],
    install_requires=[''],
    url='https://github.com/tudstlennkozh/maylibre/',
    license='Apache 2.0',
    author='tudstlennkozh',
    author_email='',
    description='Eases mailing from LibreOffice to an Exchange server'
)
