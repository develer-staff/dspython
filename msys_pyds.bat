SET PATH=C:\MinGW\bin;C:\devkitPro\msys\bin;c:\devkitPro\devkitARM\bin;c:\Python24\;c:\Python24\Scripts

SET INCLUDE=/c/devkitPro/devkitARM/arm-eabi/include
SET LIB=/c/devkitPro/devkitARM/arm-eabi/lib

SET DEVKITPRO=/c/devkitPro/
SET DEVKITARM=/c/devkitPro/devkitARM/


rem ndslib

SET NDSLIB_INCLUDE=c:\devkitPro\libnds\include
SET NDSLIB_LIB=c:\devkitPro\libnds\lib


rem stackless

set BASECFLAGS=-ffast-math -mthumb -mthumb-interwork -DARM9 -DNDS
set CFLAGS=-ffast-math -mthumb -mthumb-interwork -DARM9 -DNDS
set LDFLAGS=-specs=ds_arm9.specs -g -mthumb -mthumb-interwork

set CC_FOR_BUILD=gcc

set PYTHON_FOR_BUILD=/c/Python24/python


c:\devkitPro\msys\msys.bat