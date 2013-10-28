/*
 * luna.c:
 *	Interface to Laika Luna hardware module
 *
 * Copyright (c) 2013 Andy Bakin. <www.project-laika.com>
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

unsigned char luna_output(unsigned char module_id_lower_two_bits, unsigned char output_state_1, unsigned char output_state_2, unsigned int* buffer_in)
{
	ret = ftdi_write_data_set_chunksize(&ftdic, 6);
	ret = ftdi_read_data_set_chunksize(&ftdic, 1);

	buf[0] = SYNC_BYTE;
	buf[1] = (LUNA_ID | (module_id_lower_two_bits & MODULE_ID_MASK));				//module id
	buf[2] = WRITE_TWO_BYTES;														//command 1: number of bytes to write + wr(bit0 = 0)
	buf[3] = LUNA_OUTPUT_SET;														//command 2: function
	buf[4] = output_state_1;														//Output 1
	buf[5] = output_state_2;														//output 2

	ftdi_write_data(&ftdic, buf, 6); 												//Write data over USB

	while((ret = ftdi_read_data(&ftdic, buf, LK_BUFFER_SIZE)) == 0);				//Wait for ACK
	
	buffer_in[0] = (int)buf[0];
	
	return ret;
}

