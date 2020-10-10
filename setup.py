from setuptools import find_packages, setup

from pokemon_api import __version__

setup(
    name="pokemon_api",
    version=__version__,
    url="https://github.com/magocod/dj_chat",
    author="Yeison mago",
    author_email="androvirtual12@gmail.com",
    description="pokemon api, django",
    python_requires=">=3.7",
    packages=find_packages(),
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7"
    ]
)
