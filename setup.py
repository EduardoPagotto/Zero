#!./venv/bin/python3
'''
Created on 20190821
Update on 20220919
@author: Eduardo Pagotto
'''

from setuptools import setup, find_packages

from src.common import __version__ as VERSION

PACKAGE = "Zero"

setup(
    name="Zero",
    version=VERSION,
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="RPC em UnixDomainProtocol",
    long_description="RPC em UnixDomainProtocol e outras rotinas de IPC",#long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EduardoPagotto/Zero.git",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['typed-ast','typing-extensions', 'wheel'],
)
