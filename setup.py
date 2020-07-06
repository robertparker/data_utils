import json
from distutils.core import setup

with open('requirements.txt') as fh:
    lines = (x.split('#')[0].strip() for x in fh)
    requirements = [x for x in lines if not x == "-e ."]

setup(
    name='data_utils',
    version='0.1.0',
    description='Common utility methods I use',
    author='Rohit Parulkar',
    author_email='rohit.parulkar@gmail.com',
    url='https://example.com',
    packages=['image'],
    install_requires=requirements,
)

