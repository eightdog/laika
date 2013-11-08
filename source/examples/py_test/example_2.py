#
# example_2.py:
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
#
#   Change Log:
#               v1.0.0 - Initial release                   
#               v1.1.0 - Added lk.init() error trap
# ***********************************************************************
import time
import sys
import os

from laika import lk
from laika.explorer import exp

count = 0
ack = [0]
buffer = [None] * 32
running = True

ret = lk.init()
if (ret == lk.EXIT_FAILURE):
    print 'could not open Laika device. Exiting...'
    sys.exit()

ret = exp.dout_all(lk.MODULE_ONE, lk.OFF, ack)

while running:

	os.system("clear")
	
	print("Button 0 and 1: motors")
	print("Button 2 to exit")

	ret = exp.ain(lk.MODULE_ONE, buffer)
	
	adc_convert_1 = (buffer[0] / 4)
	adc_convert_2 = (buffer[1] / 4)
	
	print("Motor Speed 1:", adc_convert_1)
	print("Motor Speed 2:", adc_convert_2)
	
	ret = exp.din(lk.MODULE_ONE, buffer);
	button_state = buffer[0];
	print("Button Value:", button_state)

	if((button_state & exp.BUTTON_0_MASK)==0):
		ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_FORWARD, adc_convert_1, ack)
		ret = exp.dout_x(lk.MODULE_ONE, exp.OUT_0, lk.ON, ack)
	else:
		ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_STOP, adc_convert_1, ack)
		ret = exp.dout_x(lk.MODULE_ONE, exp.OUT_0, lk.OFF, ack)

	if((button_state & exp.BUTTON_1_MASK)==0):
		ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_FORWARD, adc_convert_2, ack)
		ret = exp.dout_x(lk.MODULE_ONE, exp.OUT_1, lk.ON, ack)
	else:
		ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_STOP, adc_convert_1, ack)
		ret = exp.dout_x(lk.MODULE_ONE, exp.OUT_1, lk.OFF, ack)
		
	if((button_state & exp.BUTTON_2_MASK)==0):
		running = False

lk.exit()
sys.exit()

