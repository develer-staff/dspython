SET PYTHONDIR=/c/Python26/
SET DEVKITPRO=/c/devkitPro/
SET DSPYTHON=/c/dspython/
SET MINGWDIR=/c/MinGW/

rem
rem You should not customize anything beyond this point
rem

SET DEVKITARM=%DEVKITPRO%/devkitARM/
SET PATH=%MINGWDIR%/bin;%DEVKITPRO%/msys/bin;%DEVKITARM%/bin;%PYTHONDIR%/;%PYTHONDIR%/Scripts
SET INCLUDE=%DEVKITARM%/arm-eabi/include
SET LIB=%DEVKITARM%/arm-eabi/lib

rem stackless
set ARCH=-mthumb -mthumb-interwork
set BASECFLAGS=-ffast-math %ARCH% -DARM9 -DNDS
set CFLAGS=-ffast-math %ARCH% -DARM9 -DNDS
set LDFLAGS=-specs=ds_arm9.specs -g %ARCH% -lnds9 -L%DEVKITPRO%/libnds/lib

set CC_FOR_BUILD=gcc
set PYTHON_FOR_BUILD=%PYTHONDIR%/python

c:\devkitPro\msys\msys.bat
