from setuptools import setup


def long_desc():
    with open('README.rst', 'rb') as f:
        return f.read()

kw = {
    "name": "mattdaemon",
    "version": "1.0.0",
    "description": "Easily daemonize your python projects",
    "long_description": long_desc(),
    "url": "https://github.com/plausibility/mattdaemon",
    "author": "plausibility",
    "author_email": "chris@gibsonsec.org",
    "license": "MIT",
    "packages": ['mattdaemon'],
    "zip_safe": False,
    "keywords": "daemon daemonize daemonise cli matt",
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2"
    ]
}

if __name__ == "__main__":
    setup(**kw)
