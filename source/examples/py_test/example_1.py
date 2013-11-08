#
# example_1.py:
#	Example Laika program
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
import time
import sys

from laika import lk
from laika.explorer import exp

count = 0
ack = [0]
ret = 0
buffer = [None] * 32
running = True

ret = lk.init()
if (ret == lk.EXIT_FAILURE):
    print 'could not open Laika device. Exiting...'
    sys.exit()

print "Press any button to stop"

while running:

	print count
	ret = exp.dout_all(lk.MODULE_ONE, count, ack);
	count = count + 1
	if count == 127:
		count = 0
		print "Press any button to stop"
	time.sleep(.1)

	ret = exp.din(lk.MODULE_ONE, buffer);
	if (buffer[0] != 15):
		running = False

print "Notice how the LED's represent in binary, the last number you stopped at." 
		
lk.exit()
sys.exit()

