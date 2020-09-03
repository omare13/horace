#!/usr/bin/env python
"""The setup script."""
import io
import re
from os.path import dirname
from os.path import join
from setuptools import setup, find_packages


def read(*names, **kwargs):
    with io.open(
        join(dirname(__file__), *names),
        encoding=kwargs.get('encoding', 'utf8')
    ) as fh:
        return fh.read()

readme = read('README.rst')
history = read('HISTORY.rst')
requirements = read('requirements.txt').split("\n")
setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest>=3', ]

setup(
    author="LINHD POSTDATA Project",
    author_email='info@linhd.uned.es',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Format converter from PoetryLab JSON to POSTDATA semantic formats",
    install_requires=requirements,
    license="Apache Software License 2.0",
    long_description='%s\n%s' % (
        re.compile('^.. start-badges.*^.. end-badges', re.M | re.S).sub('', readme),
        re.sub(':[a-z]+:`~?(.*?)`', r'``\1``', history)
    ),
    include_package_data=True,
    keywords='horace',
    name='horace',
    packages=find_packages(include=['horace', 'horace.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/linhd-postdata/horace',
    version='0.1.0',
    zip_safe=False,
)
