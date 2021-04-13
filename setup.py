from setuptools import setup, find_packages
from os import path
this_directory = path.abspath(path.dirname(__file__))

with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='dwython',
    version='0.2.1',
    description='Datawave Python API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/phrocker/dwython',
    author='Marc Parisi',

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='dwython',

    packages=find_packages(),

    install_requires=['requests', 'certifi', 'chardet', 'idna', 'urllib3'],
)
