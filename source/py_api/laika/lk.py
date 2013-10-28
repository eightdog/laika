#
# lk.py:
#	Top level Laika Python Interface
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
import ctypes 
laika = ctypes.CDLL('liblaika.so')
from ctypes import *

EXIT_FAILURE = 0
EXIT_SUCCESS = 1
MODULE_ONE = 0
MODULE_TWO = 1
MODULE_THREE = 2
MODULE_FOUR = 3
ON = 1
OFF = 0

present=0

def init():
	present = laika.lk_init()
	is_present()

def is_present():
	return present
	
def exit():
	lk_ret = laika.lk_exit()
	return lk_ret


