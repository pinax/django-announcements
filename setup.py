import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()


NAME = "pinax-announcements"
DESCRIPTION = "a Django announcements app"
AUTHOR = "Pinax Team"
AUTHOR_EMAIL = "team@pinaxproject.com"
URL = "https://github.com/pinax/pinax-announcements"


setup(
    name=NAME,
    version="1.2.0",
    description=DESCRIPTION,
    long_description=read("README.rst"),
    url=URL,
    license="MIT",
    packages=find_packages(),
    package_data={
        "pinax.announcements": [
            "templates/pinax/announcements/*.xml",
        ]
    },

    test_suite="runtests.runtests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
