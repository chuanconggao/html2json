#! /usr/bin/env python3

from setuptools import setup

url = "https://github.com/chuanconggao/html2json"
version = "0.2.4.1"

setup(
    name="html2json",

    packages=["html2json"],

    url=url,

    version=version,
    download_url=f"{url}/tarball/{version}",

    license="MIT",

    author="Chuancong Gao",
    author_email="chuancong@gmail.com",

    description="Parsing HTML to JSON",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    keywords=[
        "parser",
        "html",
        "json"
    ],
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],

    install_requires=[
        "future>=0.16.0",
        "pyquery>=1.4.0"
    ]
)
