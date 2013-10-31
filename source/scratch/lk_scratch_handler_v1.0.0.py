#
# lk_scratch_handler.py:
#	Scratch Handler for Laika. This file started life as scratchgpio_handler3.py by cymplecy/GPIO
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
import threading
import socket
import time
import sys
import struct
import datetime as dt
import shlex
import os
import math

from laika_scratch import lk_scratch

PORT = 42001
DEFAULT_HOST = '127.0.0.1'
BUFFER_SIZE = 240 #used to be 100
SOCKET_TIMEOUT = 1

def isNumeric(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    
def removeNonAscii(s): return "".join(i for i in s if ord(i)<128)
    
def getValue(searchString, dataString):
    outputall_pos = dataString.find((searchString + ' '))
    sensor_value = dataString[(outputall_pos+1+len(searchString)):].split()
    return sensor_value[0]

def sign(number):return cmp(number,0)

def parse_data(dataraw, search_string):
    outputall_pos = dataraw.find(search_string)
    return dataraw[(outputall_pos + 1 + search_string.length):].split()
    
class MyError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class ScratchListener(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.scratch_socket = socket
        self._stop = threading.Event()
        self.dataraw = ''
        
    def send_scratch_command(self, cmd):
        n = len(cmd)
        a = array('c')
        a.append(chr((n >> 24) & 0xFF))
        a.append(chr((n >> 16) & 0xFF))
        a.append(chr((n >>  8) & 0xFF))
        a.append(chr(n & 0xFF))
        self.scratch_socket.send(a.tostring() + cmd)
        
    def dFind(self,searchStr):
        return (searchStr in self.dataraw)
        
    def dFindOn(self,searchStr):
        return (self.dFind(searchStr + 'on') or self.dFind(searchStr + 'high'))
        
    def dFindOff(self,searchStr):
        return (self.dFind(searchStr + 'off') or self.dFind(searchStr + 'low'))
        
    def dFindOnOff(self,searchStr):
        return (self.dFind(searchStr + 'on') or self.dFind(searchStr + 'high') 
                or self.dFind(searchStr + 'off') or self.dFind(searchStr + 'low'))

    def dRtnOnOff(self,searchStr):
        if self.dFindOn(searchStr):
            return 1
        else:
            return 0
        
    def dVFind(self,searchStr):
        return ((searchStr + ' ') in self.dataraw)
        
    def dVFindOn(self,searchStr):
        return (self.dVFind(searchStr + 'on') or self.dVFind(searchStr + 'high')or self.dVFind(searchStr + '1'))
        
    def dVFindOff(self,searchStr):
        return (self.dVFind(searchStr + 'off') or self.dVFind(searchStr + 'low') or self.dVFind(searchStr + '0'))
        
    def dVFindOnOff(self,searchStr):
        return (self.dVFindOn(searchStr) or self.dVFindOff(searchStr))

    def dVRtnOnOff(self,searchStr):
        if self.dVFindOn(searchStr):
            return 1
        else:
            return 0


    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()

    def run(self):
        global cycle_trace
        firstRun = False #Used for testing in overcoming Scratch "bug/feature"
        firstRunData = ''
        #This is main listening routine
        lcount = 0
        while not self.stopped():

            try:
                #print "try reading socket"
                data = self.scratch_socket.recv(BUFFER_SIZE) # get the data from the socket
                dataraw = data[4:].lower() # convert all to lowercase
                #print 'Received from scratch-Length: %d, Data: %s' % (len(dataraw), dataraw)

                if len(dataraw) > 0:
                    dataraw = ' '.join([item.replace(' ','') for item in shlex.split(dataraw)])
                    self.dataraw = dataraw
                    #print dataraw

                #print 'Cycle trace' , cycle_trace
                if len(dataraw) == 0:
                    #This is probably due to client disconnecting
                    #I'd like the program to retry connecting to the client
                    #tell outer loop that Scratch has disconnected
                    if cycle_trace == 'running':
                        cycle_trace = 'disconnected'
                        break

            except (KeyboardInterrupt, SystemExit):
                #print "reraise error"
                raise
            except socket.timeout:
                #print "No data received: socket timeout"
                continue
            except:
                print "Unknown error occured with receiving data"
                continue
            
            #print "data being processed:" , dataraw
            #This section is only enabled if flag set - I am in 2 minds as to whether to use it or not!
            if firstRun == True:
                if 'sensor-update' in dataraw:
                    #print "this data ignored" , dataraw
                    firstRunData = dataraw
                    dataraw = ''
                    firstRun = False

        

                            

                        

            #Listen for Variable changes
            if 'sensor-update' in dataraw:
                print "sensor-update rcvd" , dataraw
                if 'lk_' in dataraw:
                    lk_scratch.sensor_update(dataraw) #pass message to laika
              
                
                                                            
               
                            

### Check for Broadcast type messages being received
            if 'broadcast' in dataraw:
                #print 'broadcast in data:' , dataraw
                if 'lk_' in dataraw:
                    lk_scratch.broadcast(dataraw)	#pass message to laika

                



                        


                

            if 'stop handler' in dataraw:
                cleanup_threads((listener))
                sys.exit()



def create_socket(host, port):
    while True:
        try:
            print 'Trying'
            scratch_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            scratch_sock.connect((host, port))
            break
        except socket.error:
            print "There was an error connecting to Scratch!"
            print "I couldn't find a Mesh session at host: %s, port: %s" % (host, port) 
            time.sleep(3)

    return scratch_sock

def cleanup_threads(threads):
    for thread in threads:
        thread.stop()

    for thread in threads:
        thread.join()

  
if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = DEFAULT_HOST
    host = host.replace("'", "")

cycle_trace = 'start'

while True:

    if (cycle_trace == 'disconnected'):
        print "Scratch disconnected"
        #cleanup_threads((listener))
        listener.stop()
        listener.join()
        time.sleep(1)
        cycle_trace = 'start'

    if (cycle_trace == 'start'):
        # open the socket
        print 'Starting to connect...' ,
        the_socket = create_socket(host, PORT)
        print 'Connected!'
        the_socket.settimeout(SOCKET_TIMEOUT)
        listener = ScratchListener(the_socket)
        lk_scratch.init(the_socket)
        cycle_trace = 'running'
        print "Running...."
        listener.start()

    # wait for ctrl+c
    try:

        time.sleep(0.1)
    except KeyboardInterrupt:
        cleanup_threads((listener))
        GPIO.cleanup()
        lk_scratch.exit()
        sys.exit()
        print "CleanUp complete"
        