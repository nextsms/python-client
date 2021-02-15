from distutils.core import setup

setup(
    name="nextsms",
    version="0.1",
    description='Python package to easy integration with NextSms API for bulksms',
    url='https://github.com/Kalebu/nextsms',
    download_url="https://github.com/Kalebu/nextsms/archive/0.1.tar.gz",
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
        'requests',
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
