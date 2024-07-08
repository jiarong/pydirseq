import os
from setuptools import setup, find_packages


def get_version():
    with open(
        os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "pydirseq",
            "pydirseq.VERSION",
        )
    ) as f:
        return f.readline().strip()
    

def get_description():
    with open("README.md", "r") as fh:
        long_description = fh.read()
    return long_description


def get_data_files():
    data_files = [(".", ["README.md"]), (".", ["requirements.yaml"])]
    return data_files


CLASSIFIERS = [
    "Environment :: Console",
    "Environment :: MacOS X",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT license",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Operating System :: MacOS :: MacOS X",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Topic :: Scientific/Engineering :: Bio-Informatics",
]

setup(
    name="pydirseq",
    packages=find_packages(),
    url="https://github.com/jiarong/pydirseq",
    python_requires=">=3.6",
    description="pydirseq provides gene-wise coverage for metaT and metaG reads",
    long_description=get_description(),
    long_description_content_type="text/markdown",
    version=get_version(),
    author="Jiarong Guo",
    author_email="pydirseq near gmail",
    data_files=get_data_files(),
    py_modules=["pydirseq"],
    #install_requires=[
    #    "snaketool-utils>=0.0.4",
    #    "snakemake>=6.12.2",
    #    "pyyaml>=6.0",
    #    "Click>=8.1.3",
    #],
    entry_points={
        "console_scripts": [
            "pydirseq=pydirseq.__main__:main"
        ]
    },
    include_package_data=True,
)
