"""Yer average Python setup, fer gram!

Reads version from gram package. The PyPi readme
is gram's module-level docstring.

"""

from setuptools import setup
import ast

from gram import __version__


with open('gram/gram.py') as f:
    gram_contents = f.read()
module = ast.parse(gram_contents)
readme_docstring = ast.get_docstring(module)

setup(
    name='gram',
    version=__version__,
    description='gram: GitHub Repo Account Manager',
    long_description=readme_docstring,
    author='Lily Mayfield',
    author_email='lily.m.mayfield@gmail.com',
    keywords='cli',
    install_requires=['docopt',],
    packages=['gram',],
    entry_points = {
        'console_scripts': [
            'gram=gram.__main__:entrypoint',
        ],
    },
    package_dir={'gram': 'gram'},
)
