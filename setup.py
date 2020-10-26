#!./venv/bin/python3
'''
Created on 20190821
Update on 20201026
@author: Eduardo Pagotto
'''

import Zero
import setuptools

PACKAGE = "Zero"
VERSION = Zero.common.__version__

setuptools.setup(
    name="Zero",
    version=VERSION,
    author="Eduardo Pagotto",
    author_email="edupagotto@gmail.com",
    description="RPC em UnixDomainProtocol",
    long_description="RPC em UnixDomainProtocol e outras rotinas de IPC",#long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EduardoPagotto/Zero.git",
    packages=setuptools.find_packages(),
    #packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=['mypy']
)
