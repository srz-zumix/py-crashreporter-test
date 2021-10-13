import os
import re
from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

f = open(os.path.join(os.path.dirname(__file__), 'pychrashreportertest/__init__.py'))
for line in f:
    if '__version__ = ' in line:
        version_ = [x for x in re.split(r"[ =']", line) if x][1]
    elif '__author__ = ' in line:
        author_ = [x for x in re.split(r"[ =']", line) if x][1]
f.close()

test_deps = [
    'importlib-metadata<2,>=0.12',
    'tox-pyenv',
    'pytest',
    'python-dotenv',
    'backtracepython',
    'bugsnag',
    'sentry-sdk',
    'raygun4py',
    'rollbar',
    'tox'
]

setup(
    name = "py-chrashreporter-test"
    , version = version_
    , author = author_
    , author_email = "zumix.cpp@gmail.com"
    , url = "https://github.com/srz-zumix/py-crashreporter-test/"
    , description = "."
    , license = "MIT"
    , platforms = ["any"]
    , keywords = ""
    , packages = ['pychrashreportertest']
    , long_description = readme
    , long_description_content_type='text/markdown'
    , classifiers = [
        "Development Status :: 1 - Planning"
        , "Topic :: Utilities"
        , "License :: OSI Approved :: MIT License"
        , "Programming Language :: Python"
        , "Programming Language :: Python :: 3.8"
        , "Programming Language :: Python :: 3.9"
    ]
    , entry_points={
        'console_scripts': [
            'pychrashreportertest = pychrashreportertest.__main__:main',
        ]
    }
    , install_requires=[]
    , tests_require=test_deps
    , test_suite="tests.test_suite"
    , extras_require={
        'test': test_deps
    }
    , python_requires=">3.5"
)
