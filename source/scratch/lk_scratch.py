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
from laika import lk
from laika.explorer import exp

ack = [0]
buffer = [None] * 32

motor_1_speed = 0
motor_2_speed = 0

def lk_init():
	lk.init()
	
def lk_exit():
	lk.exit()

def lk_broadcast(broadcast_in):

	if  'exp_motor_1_fwd' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_1, lk.MOTOR_FORWARD, motor_1_speed, ack)
		
	if  'exp_motor_1_rev' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_1, lk.MOTOR_REVERSE, motor_1_speed, ack)
	
	if  'exp_motor_1_stop' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_1, lk.MOTOR_STOP, 0, ack)
		
	if  'exp_motor_1_brake' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_1, lk.MOTOR_BRAKE, 0, ack)
		
	if  'exp_motor_2_fwd' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_2, lk.MOTOR_FORWARD, motor_2_speed, ack)
		
	if  'exp_motor_2_rev' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_2, lk.MOTOR_REVERSE, motor_2_speed, ack)
		
	if  'exp_motor_2_stop' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_2, lk.MOTOR_STOP, 0, ack)
		
	if  'exp_motor_2_brake' in dataraw:
		lk_ret = exp.motors(lk.MODULE_ONE, lk.MOTOR_2, lk.MOTOR_BRAKE, 0, ack)

	
def lk_sensor_update(sensor_update_in):

	if 'exp_dout_bin' in sensor_update_in:
		output_pos = sensor_update_in.find('exp_dout_bin')
		sensor_value = sensor_update_in[(output_pos+14):].split()
		int_value = int(sensor_value[0], 2)
		if int_value in range(127):
			exp.dout_all(MODULE_ONE, int_value, lk_ack)

	if 'exp_dout_hex' in sensor_update_in:
		output_pos = sensor_update_in.find('exp_dout_hex')
		sensor_value = sensor_update_in[(output_pos+14):].split()
		int_value = int(sensor_value[0], 16)
		if int_value in range(127):
			exp.dout_all(MODULE_ONE, int_value, lk_ack)
                        
	if 'exp_dout_int' in sensor_update_in:
		output_pos = sensor_update_in.find('exp_dout_int')
		sensor_value = sensor_update_in[(output_pos+14):].split()
		int_value = int(sensor_value[0], 10)
		if int_value in range(127):
			exp.dout_all(MODULE_ONE, int_value, lk_ack)
                        
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
		

                
                if  'lk_check_for_ack' in dataraw:
                    sensor_name = 'lk_ack'
                    bcast_str = 'sensor-update "%s" %d' % (sensor_name, lk_ack[0])
                    self.send_scratch_command(bcast_str)
                    
            
#Explorer Analogue ----------------------------------------------------------------------------------------------- 
                if  'exp_ain' in dataraw:
                    laika.exp_ain(MODULE_ONE, 1, lk_ack)
                    

    