#! python
from setuptools import setup, find_packages

setup(
    name = "coffeecup",
    version = "0.0.1",
    description = "CoffeScript WSGI Middleware",
    long_description = """
        CoffeeCup is a WSGI middleware wrapper to transparently compile CoffeeScript files (things ending in `.coffee`) into javascript.
    """,
    url = "http://tire.less.ly/hacking/coffeecup",
    
    author = "David Schoonover",
    author_email = "dsc@less.ly",
    
    py_modules = ['coffeecup'],
    # packages = ['coffeecup'],
    install_requires=[
        # "demjson>=1.4",
    ],
    keywords = [],
    classifiers = [],
    zip_safe = True,

)
