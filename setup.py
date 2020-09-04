from setuptools import setup, find_packages
from pathlib import Path

setup(
    name="foo",
    version="0.0.1",
    description="A useful module",
    author="Man Foo",
    author_email="foomail@foo.com",
    packages=find_packages(),
    install_requires=[
        l.strip() for l in Path("requirements.txt").read_text("utf-8").splitlines()
    ],
)
