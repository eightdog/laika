#
# exp.py:
#	Interface module to Laika Explorer
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
#    Change Log:
#               v1.0.0 - Initial release                   
# ***********************************************************************
import ctypes 
laika = ctypes.CDLL('liblaika.so')
from ctypes import *

ID = 0b01000100
BUTTON_0_MASK = 0b00000001 
BUTTON_1_MASK = 0b00000010 
BUTTON_2_MASK = 0b00000100 
BUTTON_3_MASK = 0b00001000 
MOTOR_1 = 1
MOTOR_2 = 2
MOTOR_STOP = 0
MOTOR_FORWARD = 1
MOTOR_REVERSE = 2
MOTOR_BRAKE = 3
OUT_0 = 0
OUT_1 = 1
OUT_2 = 2
OUT_3 = 3
OUT_4 = 4
OUT_5 = 5
OUT_6 = 6

lk_ack = c_int()
lk_buffer = (c_int*32)()

def dout_all(module_id, data_in, ack = []):
	lk_ret = laika.exp_dout_all(module_id, data_in, byref(lk_ack))
	ack[0] = lk_ack.value
	return lk_ret
	
def dout_x(module_id, pin_in, data_in, ack = []):
	lk_ret = laika.exp_dout_x(module_id, pin_in, data_in, byref(lk_ack))
	ack[0] = lk_ack.value
	return lk_ret

def din(module_id, buffer_in = []):
	lk_ret = laika.exp_din(module_id, byref(lk_buffer))
	buffer_in[0] = lk_buffer[0]
	return lk_ret

def ain(module_id, buffer_in = []):
	lk_ret = laika.exp_ain(module_id, byref(lk_buffer))
	buffer_in[0] = lk_buffer[0]
	buffer_in[1] = lk_buffer[1]
	return lk_ret
	
def motors(module_id, motor_in, direction_in, speed_in, ack = []):
	lk_ret = laika.exp_motors(module_id, motor_in, direction_in, speed_in, byref(lk_ack))
	ack[0] = lk_ack.value
	return lk_ret



