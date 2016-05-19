/*
 * exp.c:
 *	Interface to Laika Explorer hardware module
 *
 * Copyright (c) 2016 Andy Bakin. <www.project-laika.com>
 ***********************************************************************
 * This file is part of Laika:
 *	https://github.com/eightdog/laika.git
 *
 *    Laika is free software: you can redistribute it and/or modify
 *    it under the terms of the GNU Lesser General Public License as published by
 *    the Free Software Foundation, either version 3 of the License, or
 *    (at your option) any later version.
 *
 *    Laika is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU Lesser General Public License for more details.
 *
 *    You should have received a copy of the GNU Lesser General Public License
 *    along with Laika.  If not, see <http://www.gnu.org/licenses/>.
 ***********************************************************************
 */
 
#include <stdio.h>
#include <unistd.h>
#include <ftdi.h>
#include "include/laika/laika.h"

struct ftdi_context ftdic;
unsigned char buf[LK_BUFFER_SIZE];
int ret;

unsigned char exp_dout_all(unsigned char module_id_lower_two_bits, unsigned char data_in, unsigned int* buffer_in)
{
	ret = ftdi_write_data_set_chunksize(&ftdic, 5);
	ret = ftdi_read_data_set_chunksize(&ftdic, 3);
	
	buf[0] = SYNC_BYTE;
	buf[1] = (EXP_ID | (module_id_lower_two_bits & MODULE_ID_MASK));				//module id
	buf[2] = WRITE_ONE_BYTE;														//command 1: number of bytes to write + wr(bit0 = 0)
	buf[3] = EXP_DOUT_ALL;															//command 2: function
	buf[4] = data_in;

	ftdi_write_data(&ftdic, buf, 5); 												//Write data over USB

	while((ret = ftdi_read_data(&ftdic, buf, LK_BUFFER_SIZE)) == 0);				//Wait for ACK
	
	buffer_in[0] = (int)buf[0];

	return ret;

}

unsigned char exp_dout_x(unsigned char module_id_lower_two_bits, unsigned char pin_in, unsigned char data_in, unsigned int* buffer_in)
{
	ret = ftdi_write_data_set_chunksize(&ftdic, 6);
	ret = ftdi_read_data_set_chunksize(&ftdic, 3);
	
	buf[0] = SYNC_BYTE;
	buf[1] = (EXP_ID | (module_id_lower_two_bits & MODULE_ID_MASK));				//module id
	buf[2] = WRITE_TWO_BYTES;														//command 1: number of bytes to write + wr(bit0 = 0)
	buf[3] = EXP_DOUT_X;															//command 2: function
	buf[4] = pin_in;
	buf[5] = data_in;

	ftdi_write_data(&ftdic, buf, 6); 												//Write data over USB

	while((ret = ftdi_read_data(&ftdic, buf, LK_BUFFER_SIZE)) == 0);				//Wait for ACK
	
	buffer_in[0] = (int)buf[0];

	return ret;

}

unsigned char exp_din(unsigned char module_id_lower_two_bits, unsigned int* buffer_in)
{
	ret = ftdi_write_data_set_chunksize(&ftdic, 4);
	ret = ftdi_read_data_set_chunksize(&ftdic, 3);
	
	buf[0] = SYNC_BYTE;
	buf[1] = (EXP_ID | (module_id_lower_two_bits & MODULE_ID_MASK));				//module id
	buf[2] = READ_ONE_BYTE;														//command 1: number of bytes to read + rd(bit0 = 1)
	buf[3] = EXP_DIN;															//command 2: function

	ftdi_write_data(&ftdic, buf, 4); 
	
	while((ret = ftdi_read_data(&ftdic, buf, LK_BUFFER_SIZE))==0);
	
	buffer_in[0] = (int)buf[0];

	return ret;

}

unsigned char exp_ain(unsigned char module_id_lower_two_bits, unsigned int* buffer_in)
{
	ret = ftdi_write_data_set_chunksize(&ftdic, 4);
	ret = ftdi_read_data_set_chunksize(&ftdic, 6);
	
	buf[0] = SYNC_BYTE;
	buf[1] = (EXP_ID | (module_id_lower_two_bits & MODULE_ID_MASK));				//module id
	buf[2] = READ_ONE_BYTE;														//command 1: number of bytes to read + rd(bit0 = 1)
	buf[3] = EXP_AIN;															//command 2: function

	ftdi_write_data(&ftdic, buf, 4); 
	
	while((ret = ftdi_read_data(&ftdic, buf, LK_BUFFER_SIZE))==0);
	
	buffer_in[0] = (((int)(buf[0]))<<8);
	buffer_in[0] |= (int)buf[1]; 
	buffer_in[1] = (((int)(buf[2]))<<8);
	buffer_in[1] |= (int)buf[3];

	return ret;

}

unsigned char exp_motors(unsigned char module_id_lower_two_bits, unsigned char motor_in, unsigned char direction_in, unsigned char speed_in , unsigned int* buffer_in)
{
	ret = ftdi_write_data_set_chunksize(&ftdic, 7);
	ret = ftdi_read_data_set_chunksize(&ftdic, 3);
	
	buf[0] = SYNC_BYTE;
	buf[1] = (EXP_ID | (module_id_lower_two_bits & MODULE_ID_MASK));				//module id
	buf[2] = WRITE_THREE_BYTES;														//command 1: number of bytes to read + rd(bit0 = 1)
	buf[3] = EXP_MOTORS;															//command 2: function
	buf[4] = motor_in;
	buf[5] = direction_in;
	buf[6] = speed_in;
	
	ftdi_write_data(&ftdic, buf, 7); 
	
	while((ret = ftdi_read_data(&ftdic, buf, LK_BUFFER_SIZE))==0);
	
	buffer_in[0] = (int)buf[0];

	return ret;

}



