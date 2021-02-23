#!/bin/bash
echo "Executing Pyinstaller Windows..."
pip install pyinstaller
cd .\hexonet\ispapicli\
pyinstaller --onefile --windowed .\ispapicli.py
cd .\dist
New-Item -Path .\bin -ItemType Directory
Move-Item -Path .\ispapicli.exe -Destination .\bin -PassThru
Copy-Item -Path ..\commands -Destination .\ -Recurse -Force -Passthru
Copy-Item -Path ..\config -Destination .\ -Recurse -Force -Passthru
Copy-Item -Path ..\icons -Destination .\ -Recurse -Force -Passthru
cd ..
Compress-Archive -Path .\dist -DestinationPath ..\..\win-binary-latest.zip