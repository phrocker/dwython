from setuptools import setup, find_packages

setup(
    name='dwython',
    version='0.1.3',
    description='Datawave Python API',
    url='https://github.com/phrocker/dwython',
    author='Marc Parisi',

    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
