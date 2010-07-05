#! python
from setuptools import setup, find_packages

setup(
    name = "coffeecup",
    version = "0.1.0",
    description = "CoffeScript WSGI Middleware",
    long_description = """
        CoffeeCup is a WSGI middleware wrapper to transparently compile CoffeeScript files at serve-time.
    """,
    url = "http://github.com/dsc/coffeecup",
    
    author = "David Schoonover",
    author_email = "dsc@less.ly",
    
    py_modules = ['coffeecup'],
    keywords = [],
    classifiers = [],
    zip_safe = True,

)
