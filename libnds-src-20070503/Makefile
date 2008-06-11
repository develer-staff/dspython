#---------------------------------------------------------------------------------
.SUFFIXES:
#---------------------------------------------------------------------------------
ifeq ($(strip $(DEVKITARM)),)
$(error "Please set DEVKITARM in your environment. export DEVKITARM=<path to>devkitARM")
endif

include $(DEVKITARM)/ds_rules

#---------------------------------------------------------------------------------
BUILD		:= build

ARM9SOURCES :=	source/arm9 source/common
ARM7SOURCES :=	source/arm7 source/common

DATESTRING	:=	$(shell date +%Y)$(shell date +%m)$(shell date +%d)

export PATH		:=	$(DEVKITARM)/bin:$(PATH)

export BASEDIR	:=	$(CURDIR)
export LIBDIR	:=	$(BASEDIR)/lib
export DEPENDS	:=	$(BASEDIR)/deps
export INCDIR	:=	$(BASEDIR)/include
export BUILDDIR	:=	$(BASEDIR)/$(BUILD)

ARM9CFILES	:=	$(foreach dir,$(ARM9SOURCES),$(notdir $(wildcard $(dir)/*.c)))
ARM9SFILES	:=	$(foreach dir,$(ARM9SOURCES),$(notdir $(wildcard $(dir)/*.s)))
ARM9BINFILES	:=	$(foreach dir,$(ARM9SOURCES),$(notdir $(wildcard $(dir)/*.bin)))

ARM7CFILES	:=	$(foreach dir,$(ARM7SOURCES),$(notdir $(wildcard $(dir)/*.c)))
ARM7SFILES	:=	$(foreach dir,$(ARM7SOURCES),$(notdir $(wildcard $(dir)/*.s)))

export ARM9_VPATH	:=	$(foreach dir,$(ARM9SOURCES),$(BASEDIR)/$(dir))
export ARM7_VPATH	:=	$(foreach dir,$(ARM7SOURCES),$(BASEDIR)/$(dir))

export ARM9OBJS :=	$(ARM9BINFILES:.bin=.o) $(ARM9CFILES:.c=.o) $(ARM9SFILES:.s=.o)
export ARM9INC	:=	-I$(BUILDDIR)/arm9
export ARM7OBJS :=	$(ARM7CFILES:.c=.o) $(ARM7SFILES:.s=.o)
export ARM7INC	:=	-I$(BUILDDIR)/arm7

export ARCH	:=	-mthumb -mthumb-interwork

export ARM9FLAGS	:=	$(ARCH) -march=armv5te -mtune=arm946e-s -DARM9
export ARM7FLAGS	:=	$(ARCH) -mcpu=arm7tdmi -mtune=arm7tdmi -DARM7

export BASEFLAGS	:=	-g -Wall -O2\
				-fomit-frame-pointer\
				-ffast-math \
				-I$(INCDIR) \
				-I/c/dspython/slp-250/Include \
				-I/c/dspython/slp-250 \
				-I/c/dspython/slp-250/Stackless


.PHONY:	all dist docs clean lib/libnds9.a  lib/libnds7.a

#---------------------------------------------------------------------------------
all:	wrappers lib/libnds9.a  basic.arm7
#---------------------------------------------------------------------------------

# wrappers

wrappers: source/arm9/wrap_console.c \
          source/arm9/wrap_video.c \
		  source/arm9/wrap_videoGL.c \
		  source/arm9/wrap_system.c \
		  source/arm9/wrap_interrupts.c \
		  source/arm9/wrap_rumble.c \
		  source/arm7/wrap_touch.c

PYTHON := python
PYREXC := /c/Python24/Scripts/pyrexc.py

source/arm9/wrap_console.c: include/nds/arm9/wrap_console.pyx
	$(PYTHON) $(PYREXC) include/nds/arm9/wrap_console.pyx -o source/arm9/wrap_console.c

source/arm9/wrap_video.c: include/nds/arm9/wrap_video.pyx
	$(PYTHON) $(PYREXC) include/nds/arm9/wrap_video.pyx -o source/arm9/wrap_video.c

source/arm9/wrap_videoGL.c: include/nds/arm9/wrap_videoGL.pyx
	$(PYTHON) $(PYREXC) include/nds/arm9/wrap_videoGL.pyx -o source/arm9/wrap_videoGL.c

source/arm9/wrap_system.c: include/nds/wrap_system.pyx
	$(PYTHON) $(PYREXC) include/nds/wrap_system.pyx -o source/arm9/wrap_system.c

source/arm9/wrap_interrupts.c: include/nds/wrap_interrupts.pyx
	$(PYTHON) $(PYREXC) include/nds/wrap_interrupts.pyx -o source/arm9/wrap_interrupts.c

source/arm9/wrap_rumble.c: include/nds/arm9/wrap_rumble.pyx
	$(PYTHON) $(PYREXC) include/nds/arm9/wrap_rumble.pyx -o source/arm9/wrap_rumble.c

source/arm7/wrap_touch.c: include/nds/arm7/wrap_touch.pyx
	$(PYTHON) $(PYREXC) include/nds/arm7/wrap_touch.pyx -o source/arm7/wrap_touch.c
	
#---------------------------------------------------------------------------------
lib/libnds9.a: lib $(DEPENDS)/arm9 $(BUILD)/arm9
#---------------------------------------------------------------------------------
	@$(MAKE) -C $(BUILD)/arm9 -f $(BASEDIR)/Makefile.arm9

#---------------------------------------------------------------------------------
lib/libnds7.a: lib $(DEPENDS)/arm7 $(BUILD)/arm7
#---------------------------------------------------------------------------------
	@$(MAKE) -C $(BUILD)/arm7 -f $(BASEDIR)/Makefile.arm7

#---------------------------------------------------------------------------------
$(BUILD)/arm7:
#---------------------------------------------------------------------------------
	mkdir -p $@
#---------------------------------------------------------------------------------
$(BUILD)/arm9:
#---------------------------------------------------------------------------------
	mkdir -p $@
#---------------------------------------------------------------------------------
$(DEPENDS)/arm7:
#---------------------------------------------------------------------------------
	mkdir -p $@/arm7
#---------------------------------------------------------------------------------
$(DEPENDS)/arm9:
#---------------------------------------------------------------------------------
	mkdir -p $@/arm9

#---------------------------------------------------------------------------------
lib:
#---------------------------------------------------------------------------------
	mkdir -p lib

#---------------------------------------------------------------------------------
clean:
#---------------------------------------------------------------------------------
	rm -fr $(DEPENDS) $(BUILD) *.bz2 source/arm9/wrap_*.c source/arm7/wrap_*.c
	$(MAKE) TARGET=$(CURDIR)/basic -C basicARM7 clean

#---------------------------------------------------------------------------------
dist: all dist-src dist-bin
#---------------------------------------------------------------------------------

dist-src:
	@tar	--exclude=*CVS* -cvjf libnds-src-$(DATESTRING).tar.bz2 source include \
			basicARM7/Makefile basicARM7/source libnds_license.txt Makefile Makefile.arm9 Makefile.arm7

dist-bin: lib/libnds9.a  basic.arm7
	@tar --exclude=*CVS* -cvjf libnds-$(DATESTRING).tar.bz2 include lib libnds_license.txt basic.arm7

#---------------------------------------------------------------------------------
install: dist-bin
#---------------------------------------------------------------------------------
	mkdir -p $(DEVKITPRO)/libnds
	bzip2 -cd libnds-$(DATESTRING).tar.bz2 | tar -xvf - -C $(DEVKITPRO)/libnds

#---------------------------------------------------------------------------------
docs:
#---------------------------------------------------------------------------------
	doxygen libnds.dox
	cat warn.log

#---------------------------------------------------------------------------------
basic.arm7: lib/libnds7.a
#---------------------------------------------------------------------------------
	@$(MAKE) -C basicARM7 TARGET=$(CURDIR)/basic LIBNDS=$(CURDIR)
