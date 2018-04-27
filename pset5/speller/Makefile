# The line below defines a variable called CC that specifies that make should use clang for compiling.
# compiler to use
CC = clang

# The line below defines a variable called CFLAGS that specifies, in turn, that clang should use some flags, most of which should look familiar.
# flags to pass compiler
CFLAGS = -ggdb3 -O0 -Qunused-arguments -std=c11 -Wall -Werror

# The line below defines a variable called EXE, the value of which will be our program’s name.
# name for executable
EXE = speller

# The line below defines a variable called HDRS, the value of which is a space-separated list of header files used by speller.
# space-separated list of header files
HDRS = dictionary.h

# space-separated list of libraries, if any,
# each of which should be prefixed with -l (e.g. -lcs50 for cs50 library)
LIBS =

#The line below defines a variable called SRCS, the value of which is a space-separated list of C files that will collectively implement speller.
# space-separated list of source files
SRCS = speller.c dictionary.c

# The line below defines a variable called OBJS, the value of which is identical to that of SRCS, except that each file’s extension is not .c but .o.
# automatically generated list of object files		// object, the value of which is indetical to SRCS but with file extension .o, not .c
OBJS = $(SRCS:.c=.o)

# The lines below define a "target" using these variables that tells make how to compile speller.
# default target
$(EXE): $(OBJS) $(HDRS) Makefile
	$(CC) $(CFLAGS) -o $@ $(OBJS) $(LIBS)

# The line below specifies that our .o files all "depend on" dictionary.h and Makefile so that changes to either induce recompilation of the former when you run make.
# dependencies 
$(OBJS): $(HDRS) Makefile

# Finally, the lines below define another target for cleaning up this problem’s directory.
# housekeeping
clean:
	rm -f core $(EXE) *.o
