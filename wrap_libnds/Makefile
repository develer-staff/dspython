include $(DEVKITARM)/ds_rules

export CFLAGS	:=	-Wall -O2\
				-fomit-frame-pointer\
				-ffast-math \
				-I$(DEVKITPRO)/libnds/include \
				-I$(DSPYTHON)/slp-250/Include \
				-I$(DSPYTHON)/slp-250 \
				-I$(DSPYTHON)/slp-250/Stackless \
				$(ARCH) \
				-DNDS

export DEPSDIR	:=	$(CURDIR)

.PHONY: clean

#all: wrappers9 wrappers7
#	ar rc libpynds.a source/arm9/wrap_*.o source/arm7/wrap_*.o

all: lib9 lib7

lib9: wrappers9
	cp $(DEVKITPRO)/libnds/lib/libnds9.a .
	ar r libnds9.a source/arm9/wrap_*.o

lib7: wrappers7
	cp $(DEVKITPRO)/libnds/lib/libnds7.a .
	ar r libnds7.a source/arm7/wrap_*.o

wrappers9:
	$(MAKE) -f Makefile.arm9

wrappers7:
	$(MAKE) -f Makefile.arm7

clean:
	#rm -rf source/arm9/*.c source/arm9/*.o source/arm9/*.d source/arm7/*.c source/arm7/*.o source/arm7/*.d libpynds.a
	rm -rf source/arm9/*.c source/arm9/*.o source/arm9/*.d source/arm7/*.c source/arm7/*.o source/arm7/*.d libnds9.a libnds7.a
