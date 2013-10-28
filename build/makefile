DESTDIR=
PREFIX=/usr

VER_MAJOR=1
VER_MINOR=0
VER_BUG=0

CC = gcc
LIBS = -lc -lftdi -lusb
DYNAMIC=liblaika.so

SRCDIR=../source

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
	@mkdir $(DESTDIR)$(PREFIX)/include/laika
	@install -m 0775 -d										$(DESTDIR)$(PREFIX)/include/laika
	@install -m 0644 $(SRCDIR)/c_api/include/laika/laika.h	$(DESTDIR)$(PREFIX)/include/laika
	@install -m 0644 $(SRCDIR)/c_api/include/laika/exp.h	$(DESTDIR)$(PREFIX)/include/laika
	@install -m 0644 $(SRCDIR)/c_api/include/laika/luna.h	$(DESTDIR)$(PREFIX)/include/laika
	@echo "[Headers Installed]"
	
.PHONEY: install
install: $(DYNAMIC) install-headers
	@echo "[Install Dynamic Library]"
	@install -m 0755 -d										$(DESTDIR)$(PREFIX)/lib
	@install -m 0755 $(LIB_RELEASE)							$(DESTDIR)$(PREFIX)/lib
	@ln -sf $(DESTDIR)$(PREFIX)/lib/$(LIB_RELEASE)			$(DESTDIR)/lib/$(DYNAMIC)
	@ln -sf $(DESTDIR)/lib/$(DYNAMIC)						$(DESTDIR)/lib/$(LIB_MAJOR)
	@ln -sf $(DESTDIR)/lib/$(LIB_MAJOR)						$(DESTDIR)/lib/$(LIB_MINOR)
	@echo "[Dynamic Library Installed]"
	@ldconfig

.PHONEY: uninstall
uninstall:
	@echo "[Uninstall Laika]"
	@rm -f $(PREFIX)/include/laika/laika.h
	@rm -f $(PREFIX)/include/laika/exp.h
	@rm -f $(PREFIX)/include/laika/luna.h
	@rm -f $(PREFIX)/lib/$(LIB_RELEASE)
	@rm -f $(PREFIX)/lib/$(DYNAMIC)
	@rm -f $(PREFIX)/lib/$(LIB_MAJOR)
	@rm -f $(PREFIX)/lib/$(LIB_MINOR)
	@rm -f $(PREFIX)/include/laika -R

laika.o: $(SRCDIR)/c_api/include/laika/laika.h
exp.o: $(SRCDIR)/c_api/include/laika/exp.h
luna.o: $(SRCDIR)/c_api/include/laika/luna.h

