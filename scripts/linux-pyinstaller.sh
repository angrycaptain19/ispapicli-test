#!/bin/bash
echo "Executing Pyinstaller Ubuntu..."
pip install pyinstaller
cd hexonet/ispapicli || exit
pyinstaller --onefile ispapicli.py
cd dist
sudo chmod +x ispapicli
mkdir bin
mv ispapicli bin
cp -r ../commands ../icons ../config .
cd ..
zip -r linux-binary-latest.zip dist
mv linux-binary-latest.zip ../../