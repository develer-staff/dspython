ifeq ($(strip $(DEVKITPRO)),)
$(error "Please set DEVKITPRO in your environment. export DEVKITPRO=<path to>devkitPro)
endif
 
export TOPDIR	:=	$(CURDIR)
 
export DATESTRING	:=	$(shell date +%Y)$(shell date +%m)$(shell date +%d)

default: release

all: release dist

lib:
	@[ -d $@ ] || mkdir -p $@

release: lib
	make -C nds BUILD=release

debug: lib
	make -C nds BUILD=debug

clean:
	make -C nds clean

dist-bin: release distribute/$(DATESTRING)
	make -C nds dist-bin

dist-src: distribute/$(DATESTRING)
	@tar --exclude=*CVS* -cvjf distribute/$(DATESTRING)/libfat-src-$(DATESTRING).tar.bz2 \
	source include Makefile \
	nds/Makefile nds/include

dist: dist-bin dist-src

distribute/$(DATESTRING): distribute
	@[ -d $@ ] || mkdir -p $@

distribute:
	@[ -d $@ ] || mkdir -p $@

install: dist
	make -C nds install
