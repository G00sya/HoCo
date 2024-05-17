#!/bin/bash

# Update package lists and install required packages
apt-get update
apt-get install -y git cmake python3 python3-pip

python3 -m venv ../env
source ../env/bin/activate
pip install -r ../requirements.txt

# Clone CocoRPy3 repository and install CocoR
git clone https://github.com/hb9chm/CocoRPy3
cd CocoRPy3
pip install build
python -m build
pip install ./dist/CocoRPy3-3.1.0-py3-none-any.whl
cd ..
coco ../src/parser/grammar.atg
python3 cocor_corrector.py
#cp Parser.py ../src/parser/Parser.py

