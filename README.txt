== dspython ==

This package contains the full source code and instructions to build Python
for Nintendo DS, with a wrapper for libnds.

Author: Lorenzo Mancini
Email: lmancini@develer.com
Website: http://www.develer.com/trac/dspython


== How to use ==

Download ndspython.nds and place it in the root of your homebrew storage
device; it's already patched for Supercard SD, but you might want to repatch it
as your own homebrew device requires. Download main.py, change and experiment
with it as you wish, then place main.py in the /python directory in your
homebrew storage device.

Finally, run ndspython.nds as you would do with any ds rom.


== Credits ==

 * Richard Tew did the original work of porting Stackless Python 2.5 on Nintendo
DS; this project is a continuation of his work.  Please see README.old in this
same package for a list of the original credits.

 - http://www.disinterest.org/NDS/Python25.html


 * Greg Ewing is the author of Pyrex, the extension language on which dspython
bases its libnds wrapper.

 - http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/


== Preparing the environment ==

The following steps detail how to setup a development environment to rebuild
dspython.  All of the following assumes you are using a Windows O.S., but
I got reports of people successfully building the project under various Linux
flavors.

*Please* note that if you just want to write scripts with dspython and you
don't want to develop dspython itself (e.g. adding new wrappers, supporting
more libraries, etc...) then you should stop reading here and read the section
"How to use" instead.

Still here? Well.

=== Devkitpro ===

Install DevkitPro's DevkitARM: this is a port of gcc compiler for the ARM CPU
used in Nintendo DS and Gameboy Advance.  An automated installer is available.

http://sourceforge.net/projects/devkitpro/

Select install type "devkitarm" and uncheck:
 - libgba
 - libfat-gba
 - maxmodgba
 - libmirko
 - gba examples
 - gp32 examples
 - programmer's notepad
 - insight

Install in c:\devkitPro .


=== Mingw ===

A gcc for the build platform is required in order to compile python.  An
automated installer is available.

http://sourceforge.net/project/mingw

Installing:
      C Compiler
      C++ Compiler
      MSYS Basic System
      MinGW Developer Toolkit

Using pre-packaged repository catalogues (20100909)

Destination location:
      C:\MinGW


=== Python ===

You need a python to build another python :) Any version will do, I use 2.6 .

Install in c:\Python26


=== pyrex ===

Extension language used to wrap libnds.

http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/

Tested with version 0.9.9 .

Unpack and execute

python setup.py bdist_wininst

this will use distutils facilities to create a nice installer in dist/;
install pyrex with such installer.

(note: I have experienced weird random crashes of dspython if cython is used
instead of pyrex, but never investigated them - long story short, just use
pyrex at least on your first try)


== Actual building process ==

A note for the faint of heart: this process is the result of many 
trial-and-error sessions, makefile and configure rules hacking to get some
file linked and some other not, and carelessly ignoring many errors just to
get the damn thing to run. I've made my best to make sure that version bumps
of the tools used don't break the build process, and that these instructions
will be consistent between windows versions, but that's it.

In other words, don't expect flowers smiles and honey, it's more like howling
naked in a night of full moon while stipulating an unholy alliance with evil
forces, and it's still not close enough but it gives you an idea ;)

Execute all the following steps in the console environment created by
msys_pyds.bat file.


=== Compile zlib ===

cd zlib-1.2.3
make

=== Compile libpython ===

cd slp-250
sh configure --host=arm-eabi --config-cache
make libpython2.5.a

During make, on some machines pgen has been reported to crash. Just ignore it.

=== Alter devkitarm linker settings ===

We need to alter linker settings so that Python gets enough stack to run on DS.

Edit $(DEVKITARM)\arm-eabi\lib\ds_arm9.mem and change:

ewram	: ORIGIN = 0x02000000, LENGTH = 4M - 4k
to
ewram	: ORIGIN = 0x02000000, LENGTH = 4M - 260k

Edit $(DEVKITARM)\arm-eabi\lib\ds_arm9.ld and change:

__sp_usr	=	__sp_irq - 0x100;
to
__sp_usr	=	__ewram_end + 0x40000;

=== Compile libnds wrappers ===

cd wrap_libnds/
make

=== Compile NDSPython ===

cd NDSPython
make

TODO: document how to put files in a nitrofs, so that the .nds file can be run
in an emulator.
