# The MIT License (MIT)
# Copyright © 2023 Yuma Rao
# TODO(developer): Set your name
# Copyright © 2023 <your name>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the “Software”), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to the following
# conditions:

# The above copyright notice and this permission notice shall be included in all copies
# or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import re
import os
import codecs
from os import path
from io import open
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# loading version from setup.py
with codecs.open(
    os.path.join(here, "market_price/__init__.py"), encoding="utf-8"
) as init_file:
    version_match = re.search(
        r"^__version__ = ['\"]([^'\"]*)['\"]", init_file.read(), re.M
    )
    if version_match is None:
        raise ValueError("Version string not found in __init__.py")
    version_string = version_match.group(1)

setup(
    name="market_price_movement_prediction",
    version=version_string,
    description="Calculated rolling connectedness and input LSTM model for prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YCChenVictor/bittensor-subnet-market-price",
    author="YCChenVictor",
    packages=find_packages(),
    include_package_data=True,
    author_email="victor.yccchen1@gmail.com",
    license="MIT",
    python_requires=">=3.8",
    install_requires=[
        "starlette==0.37.2",
        "pydantic==2.9.2",
        "rich==13.9.2",
        "pytest==8.3.3",
        "torch==2.4.1",
        "numpy==2.0.1",
        "setuptools==70.0.0",
        "pytest-cov==5.0.0",
        "pandas==2.2.3",
        "multi-time-series-connectedness==0.2.1",
        "tensorflow==2.18.0rc2",
        "yfinance==0.2.44",
        "flake8==7.1.1",
        "black==24.10.0",
        "mypy==1.13.0",
        "bittensor==8.2.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
