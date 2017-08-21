import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "ncc_parse",
    version = "0.2",
    author = "Tom Pusateri",
    author_email = "pusateri@bangj.com",
    description = ("Parse NCC log files"),
    zip_safe=False,
    license = "MIT",
    keywords = "ncc log",
    url = "http://github.com/pusateri/ncc",
    packages=['ncc_parse'],
    long_description=read('ncc_parse/README.md'),
)
