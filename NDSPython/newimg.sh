#!/bin/bash

cd fcsrimage
cmd /c "build.bat python.img fcsr"
mv python.img ..
cd ..
rm NDSPython_fs.ds.gba
rm NDSPython_fs.nds
make
