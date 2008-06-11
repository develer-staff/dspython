== dspython ==

This package contains the full source code and instructions to build Python
for Nintendo DS, with a pyrex wrapper for libnds.

Author: Lorenzo Mancini
Email: lmancini@develer.com
Website: http://www.develer.com/~lmancini/dspython


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
used in Nintendo DS and Gameboy Advance.

http://sourceforge.net/project/showfiles.php?group_id=114505&package_id=160396

Tested with version 1.4.4; select install type "devkitarm" and uncheck:
 - libgba
 - libfat-gba
 - libmirko
 - gba examples
 - gp32 examples
 - programmer's notepad
 - insight

Install in c:\devkitpro .


=== Mingw ===

A gcc for the build platform is required in order to compile python.

http://sourceforge.net/project/showfiles.php?group_id=2435&package_id=240780

Tested with version 5.1.3; select "candidate version of MinGW" (which installs
a ported version of gcc 3.4.5), install type "minimal" and check:

 + g++
 + mingw make

Install in c:\mingw .


=== msysdtk ===

Some additional unix-like tools to build python.

http://sourceforge.net/project/showfiles.php?group_id=2435&package_id=67879&release_id=131044

Tested with version 1.0.1.

Install in C:\devkitPro\msys\1.0 , then move all the contents of directory
"1.0" in C:\devkitPro\msys (yes, overwrite anytime).

Now download msys-autoconf 2.59, msys-automake 1.8.2 from the same source.
Unpack them and again move all the contents in C:\devkitPro\msys (overwrite
anytime).


=== Python ===

You need a python to build another python :) Any version will do, I use 2.4 .

Install in c:\Python24


=== pyrex ===

Extension language used to wrap libnds.

http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/

Tested with version 0.9.5.1 .

Unpack and execute

python setup.py bdist_wininst

this will use distutils facilities to create a nice installer in dist/;
install pyrex with such installer.


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

This will stop with an error while trying to link the example, but this doesn't
matter since we already have libz.a .


=== Compile libpython ===

cd slp-250
sh configure --host=arm-eabi --config-cache

Now edit modules/Setup with your favourite text editor, and comment away (with
#'s) the lines about a set of modules to be statically linked to libpython.
They are about modules posix, errno, pwd, _sre, _codecs; around line 112.

make

During make, on some machines pgen has been reported to crash. Just ignore it.

This will then stop with an error while linking the python executable, which
is useless to us since we already have libpython2.5.a .


=== Alter devkitarm linker settings ===

We need to alter linker settings so that Python gets enough stack to run on DS.

Edit c:\devkitPro\devkitARM\arm-eabi\lib\ds_arm9.ld and change:

ewram	: ORIGIN = 0x02000000, LENGTH = 4M - 4k
to
ewram	: ORIGIN = 0x02000000, LENGTH = 4M - 260k

and

__sp_usr	=	__sp_irq - 0x100;
to
__sp_usr	=	__ewram_end + 0x40000;

=== Compile libnds with wrappers ===

cd libnds-src-20070503/
make && make

=== Compile libfat ===

cd libfat-src-20070127/
make

=== (optional) Create a fat12 fcsr image file ===

To run dspython in an emulator, you can create a fat12 fcsr filesystem image file
that contains the scripts you would otherwise place in your homebrew storage
device.  To do this:

Place your scripts in NDSPython/fcsrimage/fcsr/python .  This folder already
contains a main.py, which you can replace with your own.

Proceed to the next step.  The actual image file will be built later.

=== Compile NDSPython ===

If you want to generate a rom file suitable to run in an emulator using the
fcsr trick described above, typing:

cd NDSPython
sh newimg.sh

will build the fat12 image and prepare the rom.


Instead, if you just want to build a rom to be used in actual hardware, this
will be enough:

cd NDSPython
make
