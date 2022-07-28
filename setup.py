"""
Flask-Simple-Auth
-------------

This is a "SIMPLE" Authentication Module for "fast food equivalent" speed development
"""
from setuptools import setup


setup(
    name='Flask-Simple-Auth',
    version='1.0',
    license='BSD',
    author='Trần Ngọc Trai',
    author_email='traitn.dev@gmail.com',
    description='This is a "SIMPLE" Authentication Module for "fast food equivalent" speed development',
    long_description=__doc__,
    py_modules=['flask_simple_auth'],
    # if you would be using a package instead use packages instead
    # of py_modules:
    # packages=['flask_sqlite3'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask',
        'SQLAlchemy'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)