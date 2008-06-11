#
# Hello, dear Stackless Python Programmer. Please correct the LIBS and INCLUDE macros.
#

LIBS = -ldl /usr/lib/libpython2.4.a /usr/lib/libboost_python-gcc-mt-1_32.so.1.32.0 -lpthread
INCLUDE= -I/usr/local/include/python2.4/

CC = g++

 .cpp.o:
	$(CC) -ggdb -O2 $(INCLUDE) -c $<

default:
	@echo "You need to modify this Makefile to contain the right paths to your python include" 
	@echo "directories and right libraries."
	@echo "Notice, that the boost.python (libboost_python....) must be compiled against"
	@echo "the stackless python."

#
# Once you have edited me, run "make main"
#

main: main.o sync.o sleeper.o
	g++ -o main main.o sync.o sleeper.o $(LIBS)
 
clean:
	rm -f main *.o

