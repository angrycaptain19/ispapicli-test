#!/bin/bash
echo "Executing Pyinstaller MacOS..."
pip install pyinstaller
cd hexonet/ispapicli || exit
pyinstaller --onefile ispapicli.py
cd dist
sudo chmod +x ispapicli
mkdir bin
mv ispapicli bin
cp -r ../commands ../icons ../config .
cd ..
zip -r macos-binary-latest.zip dist
mv macos-binary-latest.zip ../../