from setuptools import setup, find_packages
import os
import codecs

with open("README.md") as file:
    long_description = file.read()


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), "r") as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith("__version__"):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
        if line.startswith("__dev__"):
            delim = '"' if '"' in line else "'"
            dev = line.split(delim)[1]

    try:
        if len(dev) == 0:
            return version
        else:
            return version + "-" + dev
    except:
        raise RuntimeError("Unable to find version string in {}.".format(rel_path))


with open("requirements.txt", "r") as f:

    REQUIREMENTS = [line for line in f.read().splitlines() if len(line) > 0]



setup(
    name="airfoilGenerator",
    version=get_version("airfoil_generator/__init__.py"),
    description="Airfoil toolkit for generating and manipulating airfoil geometries",
    long_description=long_description,
    url="",
    author="Shaun Pullin",
    author_email="sp16189@bristol.ac.uk",
    license="MIT",
    install_requires=REQUIREMENTS,
    packages=find_packages(exclude=["tests"]),
    include_package_data=True,
    keywords="",
)