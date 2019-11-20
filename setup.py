from setuptools import setup, find_packages
from os import path

setup(
    name="musical-chairs",
    version="0.0.1",
    author="Kodey Converse",
    author_email="kodey@krconv.com",
    packages=find_packages(exclude=["tests"]),
    entry_points={"console_scripts": ["watch=musical_chairs.__main__:main"]},
    install_requires=[
        "attrs",
        "beautifulsoup4",
        "boto3",
        "cachetools",
        "python-dotenv",
        "ratelimit",
        "requests",
        "schedule",
    ],
)
