SET PATH=/C/MinGW/bin;/c/devkitPro/msys/bin;/c/devkitPro/devkitARM/bin;/c/Python26;/c/Python26/Scripts

SET INCLUDE=/c/devkitPro/devkitARM/arm-eabi/include
SET LIB=/c/devkitPro/devkitARM/arm-eabi/lib

SET DEVKITPRO=/c/devkitPro/
SET DEVKITARM=/c/devkitPro/devkitARM/


rem ndslib

SET NDSLIB_INCLUDE=/C/devkitPro/dspython/libnds-1.4.6/include
SET NDSLIB_LIB=/C/devkitPro/dspython/libnds-1.4.6/lib


rem stackless
set ARCH=-mthumb -mthumb-interwork
set BASECFLAGS=-ffast-math -mthumb -mthumb-interwork -DARM9 -DNDS
set CFLAGS=-ffast-math -mthumb -mthumb-interwork -DARM9 -DNDS
set LDFLAGS=-specs=ds_arm9.specs -g -mthumb -mthumb-interwork

set CC_FOR_BUILD=gcc

set PYTHON_FOR_BUILD=/c/Python26/python


c:\devkitPro\msys\msys.bat