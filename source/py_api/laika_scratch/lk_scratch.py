#
# lk_scratch.py:
#	Scratch interface to Laika
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
from array import *
import socket

from laika import lk
from laika.explorer import exp

ack = [0]
buffer = [None] * 32

motor_1_speed = 255
motor_2_speed = 255

class lk_comms:

    def __init__(self, socket_in):
        self.this_socket = socket_in
        
    def get_socket(self):
        return self.this_socket
        
    def set_socket(self, socket_in):
        self.this_socket = socket_in
        
this_comms = lk_comms(None)

def init(socket_in):
    this_comms.set_socket(socket_in)
    lk.init()

def exit():
    lk.exit()

def broadcast(broadcast_in):

    if  'exp_motor_1_fwd' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_FORWARD, motor_1_speed, ack)
        
    if  'exp_motor_1_rev' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_REVERSE, motor_1_speed, ack)

    if  'exp_motor_1_stop' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_STOP, 0, ack)
        
    if  'exp_motor_1_brake' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_BRAKE, 0, ack)
        
    if  'exp_motor_2_fwd' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_FORWARD, motor_2_speed, ack)
        
    if  'exp_motor_2_rev' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_REVERSE, motor_2_speed, ack)
        
    if  'exp_motor_2_stop' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_STOP, 0, ack)
        
    if  'exp_motor_2_brake' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_BRAKE, 0, ack)
        
    #Explorer Analogue ----------------------------------------------------------------------------------------------- 
    if  'exp_ain_0' in broadcast_in:
        exp.ain(lk.MODULE_ONE, buffer)
        sensor_name = 'lk_exp_ain_0'
        bcast_str = 'sensor-update "%s" %d' % (sensor_name, buffer[0])
        print bcast_str
        send_scratch_command(bcast_str)
        
    if  'exp_ain_1' in broadcast_in:
        exp.ain(lk.MODULE_ONE, buffer)
        sensor_name = 'lk_exp_ain_1'
        bcast_str = 'sensor-update "%s" %d' % (sensor_name, buffer[1])
        print bcast_str
        send_scratch_command(bcast_str)        
        
    #Explorer Digital ----------------------------------------------------------------------------------------------- 
    if  'exp_din' in broadcast_in:
        exp.din(lk.MODULE_ONE, buffer) 
        sensor_name = 'lk_exp_din'
        bcast_str = 'sensor-update "%s" %d' % (sensor_name, buffer[0])
        print bcast_str
        send_scratch_command(bcast_str)


def sensor_update(sensor_update_in):

    if 'exp_dout_bin' in sensor_update_in:
        output_pos = sensor_update_in.find('exp_dout_bin')
        sensor_value = sensor_update_in[(output_pos+13):].split()
        int_value = int(sensor_value[0], 2)
        if int_value in range(127):
            exp.dout_all(lk.MODULE_ONE, int_value, ack)

    if 'exp_dout_hex' in sensor_update_in:
        output_pos = sensor_update_in.find('exp_dout_hex')
        sensor_value = sensor_update_in[(output_pos+13):].split()
        int_value = int(sensor_value[0], 16)
        if int_value in range(127):
            exp.dout_all(lk.MODULE_ONE, int_value, ack)
                        
    if 'exp_dout_int' in sensor_update_in:
        output_pos = sensor_update_in.find('exp_dout_int')
        sensor_value = sensor_update_in[(output_pos+13):].split()
        int_value = int(sensor_value[0], 10)
        if int_value in range(127):
            exp.dout_all(lk.MODULE_ONE, int_value, ack)
                        
    if 'exp_motor_1_spd' in sensor_update_in:
        output_pos = sensor_update_in.find('exp_motor_1_spd')
        sensor_value = sensor_update_in[(output_pos+17):].split()
        int_value = int(sensor_value[0], 10)
        if int_value in range(255):
            motor_1_speed = int_value
            
    if 'exp_motor_2_spd' in sensor_update_in:
        output_pos = sensor_update_in.find('exp_motor_2_spd')
        sensor_value = sensor_update_in[(output_pos+17):].split()
        int_value = int(sensor_value[0], 10)
        if int_value in range(255):
            motor_2_speed = int_value
                        
    if  'lk_check_for_ack' in sensor_update_in:
        sensor_name = 'lk_ack'
        bcast_str = 'sensor-update "%s" %d' % (sensor_name, ack[0])
        self.send_scratch_command(bcast_str)
        


def send_scratch_command(cmd):
    n = len(cmd)
    a = array('c')
    a.append(chr((n >> 24) & 0xFF))
    a.append(chr((n >> 16) & 0xFF))
    a.append(chr((n >>  8) & 0xFF))
    a.append(chr(n & 0xFF))
    this_comms.get_socket().send(a.tostring() + cmd)
        




      
                    

    