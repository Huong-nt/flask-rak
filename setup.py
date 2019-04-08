"""
Flask-Rak
-------------

Easy Rogo apps Kit integration for Flask
"""
from setuptools import setup

def parse_requirements(filename):
    """ load requirements from a pip requirements file """
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

_VERSION_ = '2019.04.08.1'
setup(
    name='Flask-Rak',
    version=_VERSION_,
    url='https://github.com/Huong-nt/flask-rak.git',
    download_url = 'https://codeload.github.com/Huong-nt/flask-rak/tar.gz/' + _VERSION_,
    license='Apache 2.0',
    author='Huong NT',
    author_email='huongnt_bk@hotmail.com',
    description='Rogo apps Kit Development for Rogo Speaker Devices in Python',
    long_description=__doc__,
    packages=['flask_rak'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=parse_requirements('requirements.txt'),
    # test_requires=[
    #     'mock',
    #     'requests'
    # ],
    # test_suite='tests',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Framework :: Flask',
        'Programming Language :: Python',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
