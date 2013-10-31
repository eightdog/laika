#
# Makefile for Laika Library and examples
#
# Copyright (c) 2013 Andy Bakin. <www.project-laika.com>
# ***********************************************************************
# This file is part of Laika:
#	https://github.com/eightdog/laika.git
#
#    Laika is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Laika is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with Laika.  If not, see <http://www.gnu.org/licenses/>.
# *********************************************************************** 

SHELL = /bin/sh

DESTDIR=
PREFIX=$(DESTDIR)/usr/local
INCLUDEDIR=$(PREFIX)/include
LIBDIR=$(PREFIX)/lib
RULESDIR=/etc/udev/rules.d
SRCDIR=../source

.SUFFIXES:
.SUFFIXES: .c .o

VER_MAJOR=1
VER_MINOR=0
VER_BUG=0

CC = gcc
LIBS = -lc -lftdi -lusb
DYNAMIC=liblaika.so

LIB_MAJOR = $(DYNAMIC).$(VER_MAJOR)
LIB_MINOR = $(LIB_MAJOR).$(VER_MINOR)
LIB_RELEASE = $(LIB_MINOR).$(VER_BUG)

LIB_SRC	=	$(SRCDIR)/c_api/laika.c		\
			$(SRCDIR)/c_api/exp.c		\
			$(SRCDIR)/c_api/luna.c
			
EXM_SRC =	$(SRCDIR)/examples/c_test/example_1.c		\
			$(SRCDIR)/examples/c_test/example_2.c		\
			$(SRCDIR)/examples/c_test/example_3.c

LIB_OBJ = $(LIB_SRC:.c=.o)
EXM_OBJ = $(EXM_SRC:.c=.o)
EXM_TGT = $(EXM_SRC:.c=)

$(LIB_OBJ): CFLAGS = -fPIC -g -c -Wall
$(EXM_OBJ): CFLAGS = -Wall
 
all:$(DYNAMIC)

$(DYNAMIC):$(LIB_OBJ)
	@echo "[Link (Dynamic Library)]"
	@$(CC) -shared -Wl,-soname,$(DYNAMIC) -o $(LIB_RELEASE) $^ $(LIBS)
	@echo "[Library Linked]"

$(EXM_TGT): %: %.o
	@echo "[Link (Examples)]"
	@$(CC) -o $@ $^ -llaika 

	
.c.o:
	@echo [Compile] $<
	@$(CC) -c $(CFLAGS) $< -o $@

.PHONEY: examples
examples: $(EXM_TGT)
	@echo "[Examples Linked]"
	
.PHONEY: clean
clean:
	@echo "[Clean]"
	@rm -f $(LIB_OBJ) $(EXM_OBJ) 
	@rm -f $(LIB_RELEASE)

.PHONEY: install-headers
install-headers:
	@echo "[Install Headers]"
	@mkdir $(INCLUDEDIR)/laika
	@install -m 0775 -d										$(INCLUDEDIR)/laika
	@install -m 0644 $(SRCDIR)/c_api/include/laika/laika.h	$(INCLUDEDIR)/laika
	@install -m 0644 $(SRCDIR)/c_api/include/laika/exp.h	$(INCLUDEDIR)/laika
	@install -m 0644 $(SRCDIR)/c_api/include/laika/luna.h	$(INCLUDEDIR)/laika
	@echo "[Headers Installed]"
	
.PHONEY: install
install: $(DYNAMIC) install-headers
	@echo "[Install Dynamic Library]"
	@install -m 0755 -d										$(LIBDIR)
	@install -m 0755 $(LIB_RELEASE)							$(LIBDIR)
	@ln -sf $(LIBDIR)/$(LIB_RELEASE)						$(LIBDIR)/$(DYNAMIC)
	@ln -sf $(LIBDIR)/$(DYNAMIC)							$(LIBDIR)/$(LIB_MAJOR)
	@ln -sf $(LIBDIR)/$(LIB_MAJOR)							$(LIBDIR)/$(LIB_MINOR)
	@echo "[Dynamic Library Installed]"
	@echo "[Installing FTDI udev Rule]"
	@sudo cp ../rules/99-lklibftdi.rules $(RULESDIR)/99-lklibftdi.rules
	@ldconfig

.PHONEY: uninstall
uninstall:
	@echo "[Uninstall Laika]"
	@rm -f $(INCLUDEDIR)/laika/laika.h
	@rm -f $(INCLUDEDIR)/laika/exp.h
	@rm -f $(INCLUDEDIR)/laika/luna.h
	@rm -f $(LIBDIR)/$(LIB_RELEASE)
	@rm -f $(LIBDIR)/$(DYNAMIC)
	@rm -f $(LIBDIR)/$(LIB_MAJOR)
	@rm -f $(LIBDIR)/$(LIB_MINOR)
	@rm -f $(INCLUDEDIR)/laika -R
	@rm -f $(RULESDIR)/99-lklibftdi.rules

laika.o: $(SRCDIR)/c_api/include/laika/laika.h
exp.o: $(SRCDIR)/c_api/include/laika/exp.h
luna.o: $(SRCDIR)/c_api/include/laika/luna.h

