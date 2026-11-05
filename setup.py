from os import path
from setuptools import setup

# read the contents of your description file

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'description.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="nextsms",
    version="0.3",
    description='Python package to easy integration with NextSms API for bulksms',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Kalebu/nextsms',
    author="Jordan Kalebu",
    author_email="isaackeinstein@gmail.com",
    license="MIT",
    packages=["nextsms"],
    keywords=[
        "nextsms",
        "python-nextsms",
        "tanzania sms",
        "nextsms-tanzania",
    ],

    install_requires=[
        'requests>=2.32.4',
        'urllib3>=2.8.0',
    ],

    python_requires=">=3.10",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
