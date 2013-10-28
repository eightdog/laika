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
import sys

from laika import lk
from laika.explorer import exp

count = 0
ack = [0]
buffer = [None] * 32
running = True

lk.init()





            if 'sensor-update' in dataraw:
                #print 'sensor update'
                if 'exp_dout_bin' in dataraw:
                    #print dataraw
                    num_of_bits = PINS
                    outputall_pos = dataraw.find('exp_dout_bin')
                    sensor_value = dataraw[(outputall_pos+14):].split()
                    int_value = int(sensor_value[0], 2)
                    if int_value in range(127):
                        lk_ret = laika.exp_dout_all(MODULE_ONE, int_value, lk_ack)

                if 'exp_dout_hex' in dataraw:
                    num_of_bits = PINS
                    outputall_pos = dataraw.find('exp_dout_hex')
                    sensor_value = dataraw[(outputall_pos+14):].split()
                    int_value = int(sensor_value[0], 16)
                    if int_value in range(127):
                        lk_ret = laika.exp_dout_all(MODULE_ONE, int_value, lk_ack)
                        
                if 'exp_dout_int' in dataraw:
                    num_of_bits = PINS
                    outputall_pos = dataraw.find('exp_dout_int')
                    sensor_value = dataraw[(outputall_pos+14):].split()
                    int_value = int(sensor_value[0], 10)
                    if int_value in range(127):
                        lk_ret = laika.exp_dout_all(MODULE_ONE, int_value, lk_ack)
                        
                for i in range(PINS):
                    physical_pin = PIN_NUM[i]
                    pin_string = 'exp_dout_' + str(physical_pin)
                    if (((pin_string + '" 1' )in dataraw) or ((pin_string + '" "on') in dataraw) or ((pin_string + '" "high') in dataraw )):
                        print str(physical_pin)
                        lk_ret = laika.exp_dout_x(MODULE_ONE, 7, 1, lk_ack)
                    else:
                        if  (((pin_string + '" 0') in dataraw) or ((pin_string + '" "off') in dataraw) or ((pin_string + '" "low') in dataraw )):
                            lk_ret = laika.exp_dout_x(MODULE_ONE, 7, 0, lk_ack)

#Broadcast Message ------------------------------------------------------------------------------------------------              

            if 'broadcast' in dataraw:
                #print 'broadcast in data:' , dataraw


                #print 'broadcasting'    

                    
#Explorer Buttons ----------------------------------------------------------------------------------------------- 
                if  'exp_din' in dataraw:   
                    lk_ret = laika.exp_din(MODULE_ONE, lk_ack)
                    #print lk_ack[0]
                    lk_ack[0] = (lk_ack[0] ^ 0x0F)
                    #print lk_ack[0]
                    sensor_name = 'exp_din_val'
                    bcast_str = 'sensor-update "%s" %d' % (sensor_name, lk_ack[0])
                    #print bcast_str
                    self.send_scratch_command(bcast_str)
                    
#Explorer Analogue ----------------------------------------------------------------------------------------------- 
                if  'exp_ain' in dataraw:
                    laika.exp_ain(MODULE_ONE, 1, lk_ack)
                    
#Explorer Motors ------------------------------------------------------------------------------------------------
                if  'exp_motors_fwd' in dataraw:
                    #print 'forward'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 1, 200, lk_ack)
                    #print lk_ack[0]
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 1, 200, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motors_rev' in dataraw:
                    #print 'reverse'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 2, 200, lk_ack)
                    #print lk_ack[0]
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 2, 200, lk_ack)
                    #print lk_ack[0]                    
                    
                if  'exp_motors_lft' in dataraw:
                    #print 'left'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 1, 230, lk_ack)
                    #print lk_ack[0]
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 2, 230, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motors_rgt' in dataraw:
                    #print 'right'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 2, 230, lk_ack)
                    #print lk_ack[0]
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 1, 230, lk_ack)                    
                    #print lk_ack[0]
                    
                if  'exp_motors_stop' in dataraw:
                    #print 'stop'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 0, 0, lk_ack)
                    #print lk_ack[0]
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 0, 0, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motor_a_fwd' in dataraw:
                    #print 'a forward'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 1, 255, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motor_a_rev' in dataraw:
                    #print 'reverse'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 2, 255, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motor_a_stop' in dataraw:
                    #print 'stop'
                    lk_ret = laika.exp_motors(MODULE_ONE, 1, 0, 255, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motor_b_fwd' in dataraw:
                    #print 'forward'
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 1, 255, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motor_b_rev' in dataraw:
                    #print 'reverse'
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 2, 255, lk_ack)
                    #print lk_ack[0]
                    
                if  'exp_motor_b_stop' in dataraw:
                    #print 'stop'
                    lk_ret = laika.exp_motors(MODULE_ONE, 2, 0, 255, lk_ack)                    
                    #print lk_ack[0]
                    
#------------------------------------------------------------------------------------------------------------
                    
                     
                    
#------------------------------------------------------------------------------------------------------------
                
                if  'lk_check_for_ack' in dataraw:
                    sensor_name = 'lk_ack'
                    bcast_str = 'sensor-update "%s" %d' % (sensor_name, lk_ack[0])
                    self.send_scratch_command(bcast_str)
                    
  
               
                #end of broadcast check
                

    