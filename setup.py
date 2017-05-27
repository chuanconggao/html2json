from setuptools import setup

setup(
    name='html2json',
    packages=['html2json'],
    version='0.1.1',
    description='Parsing HTML to JSON',
    author='Chuancong Gao',
    author_email='chuancong@gmail.com',
    url='https://github.com/chuanconggao/html2json',
    download_url='https://github.com/chuanconggao/html2json/tarball/0.1.1',
    keywords=['parser', 'html', 'json'],
    license='MIT',
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    install_requires=[
        'future>=0.16.0',
    ]
)
