#Laika Scratch Installation 
#This file began life as installer.sh for cymplecy/scratch_gpio
#
# Laika build for Scratch
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

VER_MAJOR=1
VER_MINOR=0
VER_BUG=0

DESTDIR=
PREFIX=$(DESTDIR)/$(HDIR)
LKDIR=$(PREFIX)/laika_scratch
RNSCRIPT=laika_scratch_run_v$(VER_MAJOR).$(VER_MINOR).$(VER_BUG).sh

all: install

.PHONEY: install
install:
	@sudo rm -f $(LKDIR) -R
	@mkdir -p $(LKDIR)
	@chown -R $(USERID):$(GROUPID) $(LKDIR)
	@cp lk_scratch_handler_v$(VER_MAJOR).$(VER_MINOR).$(VER_BUG).py $(LKDIR)
	@chown -R $(USERID):$(GROUPID) $(LKDIR)

	@echo "#!/bin/bash" > $(LKDIR)/$(RNSCRIPT)
	@echo "#Version 0.2 - add in & to allow simulatenous running of handler and Scratch" >> $(LKDIR)/$(RNSCRIPT)
	@echo "#Version 0.3 - change sp launches rsc.sb from \"/home/pi/Documents/Scratch Projects\"" >> $(LKDIR)/$(RNSCRIPT)
	@echo "#Version 0.4 - 20Mar13 meltwater - change to use provided name for home" >> $(LKDIR)/$(RNSCRIPT)
	@echo "#Version 1.0 - 29Oct13 sw - change to cd into simplesi_scratch_handler to run servods OK" >> $(LKDIR)/$(RNSCRIPT)
	@echo "sudo ps aux | grep 'python.*lk_scratch_handler_v1.0.0.py' | grep -v grep | awk '{print \$2}' | xargs sudo kill -9 " >> $(LKDIR)/$(RNSCRIPT)
	@echo "cd $(LKDIR)" >> $(LKDIR)/$(RNSCRIPT)
	@echo "sudo python lk_scratch_handler_v1.0.0.py &" >> $(LKDIR)/$(RNSCRIPT)
	@echo "scratch --document \"$(HDIR)/Documents/Scratch Projects/rsc.sb\" &" >> $(LKDIR)/$(RNSCRIPT)
	
	@chmod +x $(LKDIR)/$(RNSCRIPT)
	@chown -R $(USERID):$(GROUPID) $(LKDIR)/$(RNSCRIPT)
	@cp laika_scratch_v$(VER_MAJOR).$(VER_MINOR).$(VER_BUG).desktop $(HDIR)/Desktop

	@mkdir -p $(HDIR)/Documents
	@sudo chown -R $(USERID):$(GROUPID) $(HDIR)/Documents

	@mkdir -p $(HDIR)/Documents/Scratch\ Projects
	@chown -R $(USERID):$(GROUPID) $(HDIR)/Documents/Scratch\ Projects

	@cp rsc.sb $(HDIR)/Documents/Scratch\ Projects
	@cp lk_exp_example_1.sb $(HDIR)/Documents/Scratch\ Projects 
	@cp lk_exp_example_2.sb $(HDIR)/Documents/Scratch\ Projects
	@cp lk_exp_example_3.sb $(HDIR)/Documents/Scratch\ Projects
	@cp lk_exp_example_4.sb $(HDIR)/Documents/Scratch\ Projects
	@cp lk_exp_example_5.sb $(HDIR)/Documents/Scratch\ Projects
	@cp lk_exp_example_6.sb $(HDIR)/Documents/Scratch\ Projects
	@cp lk_exp_example_7.sb $(HDIR)/Documents/Scratch\ Projects
	@cp lk_exp_example_8.sb $(HDIR)/Documents/Scratch\ Projects
	
	@echo ""
	@echo "Finished."
	
.PHONEY: uninstall
uninstall:
	@sudo rm -f $(LKDIR) -R
	@echo ""
	@echo "Finished."