@echo off
REM 
REM based on davr http://blog.davr.org/ linux code and shell script
REM by Troy(GPF) http://gpf.dcemu.co.uk
REM

echo Builds a FAT disk image from a given directory.
IF "%1" == "" goto ERROR
IF "%2" == "" goto ERROR
for /f "tokens=3,4*" %%a in ( 'dir /w /s /-C %2 ^| findstr "File(s)"') do @set info=%%a
set /A size="%info%+64"
echo %size%

if /I %size% LSS 100000  (                      set /A size="100000" )

echo Creating image
mkdosfs.exe %1 %size%
bfi.exe -f=%1 %2
rem 'bless' the image so it is recognized by FCSR driver, and sets up SRAM overlay

echo Blessing image
bless.exe %1
echo "FAT12 image built as %1 from /%2"
goto :end

:ERROR
echo usage: build.bat name.img dirname
goto :end

:tobig
echo directory size to large , remove some files and try again
goto :end


:end



