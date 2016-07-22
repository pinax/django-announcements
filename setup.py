import codecs

from os import path
from setuptools import find_packages, setup


def read(*parts):
    filename = path.join(path.dirname(__file__), *parts)
    with codecs.open(filename, encoding="utf-8") as fp:
        return fp.read()

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, "rst").replace("\r","")
except (ImportError, IOError):
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: read(f)


setup(
    author="Pinax Team",
    author_email="team@pinaxproject.com",
    description="a Django announcements app",
    name="pinax-announcements",
    long_description=read_md("README.md"),
    version="2.0.4",
    url="http://github.com/pinax/pinax-announcements/",
    license="MIT",
    packages=find_packages(),
    package_data={
        "announcements": []
    },
    install_requires=[
    ],
    test_suite="runtests.runtests",
    tests_require=[
        "mock>=1.3.0",
        "django-test-plus>=1.0.11",
        "pinax-theme-bootstrap>=7.7.0",
    ],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    zip_safe=False
)
