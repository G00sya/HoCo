#!/bin/bash

# Update package lists and install required packages
apt-get update
apt-get install -y git cmake python3 python3-pip

# Clone CocoRPy3 repository and install CocoR
git clone https://github.com/hb9chm/CocoRPy3
cd CocoRPy3
pip install build
python -m build
pip install ./dist/CocoRPy3-3.0.1-py3-none-any.whl
cd ..

# Run CMake and CocoR on '*.atg' files
cmake .
make
coco *.atg
