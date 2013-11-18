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
#
#   Change Log:
#   V1.0.0  - Initial Release
#   V1.1.0  - Enabled PWM speed control functionality
#           - Add exp_dout_x function calls to allow individual output pin control 
#   V1.2.0  - Changed exp_dout to only use first exp_dout instance, and added error trap for incorrect casts in sensor-updates
#           - Fixed bug that prevent value 127 being written to digital port
# ***********************************************************************
from array import *
import socket

from laika import lk
from laika.explorer import exp

OUTPUT_PINS = 7

ack = [0]
buffer = [None] * 32

class lk_comms:

    def __init__(self, socket_in):
        self.this_socket = socket_in
        
    def get_socket(self):
        return self.this_socket
        
    def set_socket(self, socket_in):
        self.this_socket = socket_in
        
class motor_speed:

    def __init__(self):
        self.speed_1 = 255
        self.speed_2 = 255

    def set_motor_1_speed(self, speed_in):
        self.speed_1 = speed_in
        
    def set_motor_2_speed(self, speed_in):
        self.speed_2 = speed_in
        
    def get_motor_1_speed(self):
        return self.speed_1
        
    def get_motor_2_speed(self):
        return self.speed_2
        
this_comms = lk_comms(None)
this_motor_speed = motor_speed()

def init(socket_in):
    this_comms.set_socket(socket_in)
    lk.init()

def exit():
    lk.exit()
    
def broadcast(broadcast_in):

    if  'exp_motor_1_fwd' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_FORWARD, this_motor_speed.get_motor_1_speed(), ack)
        
    if  'exp_motor_1_rev' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_REVERSE, this_motor_speed.get_motor_1_speed(), ack)

    if  'exp_motor_1_stop' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_STOP, 0, ack)
        
    if  'exp_motor_1_brake' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_1, exp.MOTOR_BRAKE, 0, ack)
        
    if  'exp_motor_2_fwd' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_FORWARD, this_motor_speed.get_motor_2_speed(), ack)
        
    if  'exp_motor_2_rev' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_REVERSE, this_motor_speed.get_motor_2_speed(), ack)
        
    if  'exp_motor_2_stop' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_STOP, 0, ack)
        
    if  'exp_motor_2_brake' in broadcast_in:
        lk_ret = exp.motors(lk.MODULE_ONE, exp.MOTOR_2, exp.MOTOR_BRAKE, 0, ack)
        
    print broadcast_in
    for i in range(OUTPUT_PINS):
        if (('exp_dout_pin' + str(i)) in broadcast_in):
            output_pos = broadcast_in.find('exp_dout_pin' + str(i))
            data_list = broadcast_in[(output_pos+12):].split('_', 2)
            pin_value = int(data_list[0], 10)
            pin_state = data_list[1]
            pin_state = pin_state[:4]
            #print data_list
            #print pin_value
            #print pin_state
            if (('high' in pin_state) or ('on' in pin_state) or ('1' in pin_state)):
                #print ('Pin Value On is: ' + str(pin_value))
                lk_ret = exp.dout_x(lk.MODULE_ONE, pin_value, 1, ack)
                #print str(lk_ret)
                #print str(ack[0])
            else:
                if (('low' in pin_state) or ('off' in pin_state) or ('0' in pin_state)):
                    #print ('Pin Value Off is: ' + str(pin_value))
                    lk_ret = exp.dout_x(lk.MODULE_ONE, pin_value, 0, ack)
                    #print str(lk_ret)
                    #print str(ack[0])
       
    #Explorer Analogue ----------------------------------------------------------------------------------------------- 
    if  'exp_ain_0' in broadcast_in:
        exp.ain(lk.MODULE_ONE, buffer)
        sensor_name = 'lk_exp_ain_0'
        bcast_str = 'sensor-update "%s" %d' % (sensor_name, buffer[0])
        #print bcast_str
        send_scratch_command(bcast_str)
        
    if  'exp_ain_1' in broadcast_in:
        exp.ain(lk.MODULE_ONE, buffer)
        sensor_name = 'lk_exp_ain_1'
        bcast_str = 'sensor-update "%s" %d' % (sensor_name, buffer[1])
        #print bcast_str
        send_scratch_command(bcast_str)        
        
    #Explorer Digital ----------------------------------------------------------------------------------------------- 
    if  'exp_din' in broadcast_in:
        exp.din(lk.MODULE_ONE, buffer) 
        sensor_name = 'lk_exp_din'
        bcast_str = 'sensor-update "%s" %d' % (sensor_name, buffer[0])
        #print bcast_str
        send_scratch_command(bcast_str)


def sensor_update(sensor_update_in):

    if 'exp_dout' in sensor_update_in:
        
        type_pos = sensor_update_in.find('exp_dout')
        type_str = sensor_update_in[(type_pos+8):].split(' ',2)
        #print str(type_pos)
        #print type_str
        if '_bin' in type_str:
            try:
                int_value = int(type_str[1], 2)
            except:
                print 'error with binary type cast'
                return

        if '_hex' in type_str:
            try:
                int_value = int(type_str[1], 16)
            except:
                print 'error with hexidecimal type cast'
                return
                            
        if '_int' in type_str:
            try:
                int_value = int(type_str[1], 10)
            except:
                print 'error with integer type cast'
                return

        if int_value in range(128):
            lk_ret = exp.dout_all(lk.MODULE_ONE, int_value, ack)
                        
    if 'exp_motor_1_spd' in sensor_update_in:
        output_pos = sensor_update_in.find('exp_motor_1_spd')
        sensor_value = sensor_update_in[(output_pos+16):].split()
        try:
            int_value = int(sensor_value[0], 10)
        except:
            print 'error with integer type cast'
            return
        
        if int_value in range(256):
            this_motor_speed.set_motor_1_speed(int_value)
            
    if 'exp_motor_2_spd' in sensor_update_in:
        output_pos = sensor_update_in.find('exp_motor_2_spd')
        sensor_value = sensor_update_in[(output_pos+16):].split()
        try:
            int_value = int(sensor_value[0], 10)
        except:
            print 'error with integer type cast'
            return
        
        if int_value in range(256):
            this_motor_speed.set_motor_2_speed(int_value)
                        
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
        




      
                    

    