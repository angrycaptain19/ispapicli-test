#!/bin/bash
echo "Executing Pyinstaller Windows..."
pip install pyinstaller
cd hexonet/ispapicli || exit
pyinstaller --onefile ispapicli.py
cd dist
sudo chmod +x ispapicli
mkdir bin
mv ispapicli bin
cp -r ../commands ../icons ../config .
cd ..
zip -r win-binary-latest.zip dist
mv win-binary-latest.zip ../../