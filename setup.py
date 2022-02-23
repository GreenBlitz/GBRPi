"""
Setup file.
"""
from setuptools import setup

"""
Run the following command to create a Python wheel file (installation file):

python setup.py bdist_wheel

Then run the following command to install it:

python -m pip install -U --force-reinstall dist/<NAME_OF_OUTPUT_FILE>.whl
"""

setup(
    name='gbrpi',
    version='0.0.8',
    description='A python library for Raspberry Pi operations used for FRC',
    license='Apache License 2.0',
    packages=['gbrpi',
              'gbrpi/electronics',
              'gbrpi/net',
              'gbrpi/serial',
              'gbrpi/constants'],
    author='Ido Heinemann',
    author_email='idohaineman@gmail.com',
    keywords=['rpi', 'raspberry pi', 'frc'],
    url='https://github.com/GreenBlitz/GBRPi',
    download_url='https://github.com/GreenBlitz/GBRPi/archive/v0.0.4.tar.gz',
    install_requires=[
        'pynetworktables',
        'pigpio',
        'pyserial'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

        'Intended Audience :: Developers',  # Define that your audience are developers

        'Programming Language :: Python :: 3',  # Specify which python versions that you want to support
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10'
    ],
)
