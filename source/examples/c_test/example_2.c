/*
 * example_2.c:
 *	Example Laika program
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
#include <time.h>
#include "laika/laika.h"

void display_return_code(unsigned char return_in);

void display_return_code(unsigned char return_in)
{
	if(return_in > 0)
	{
		fprintf(stderr, "Success Bytes Read: %d\n", return_in);		
	}
	else
	{
		if(return_in == 0)
		{
			fprintf(stderr, "No Data\n");
			//No Data
		}
		else
		{
			fprintf(stderr, "Error from Bulk Transfer: %d\n", return_in);
		}
	}


}


int main(void)
{
	unsigned int ret;
	unsigned char running;
	unsigned int lk_buffer[LK_BUFFER_SIZE];
	struct timespec ts;
	
	lk_init();
	
	running = 1;
	ts.tv_nsec = 500000000;
	
	while(running)
	{
		ret = exp_ain(MODULE_ONE, lk_buffer);
		display_return_code(ret);
		fprintf(stderr, "ADC 0: %x \n",  lk_buffer[0]);
		fprintf(stderr, "ADC 1: %x \n",  lk_buffer[1]);
		
		ret = exp_din(MODULE_ONE, lk_buffer);
		fprintf(stderr, "Button Value: %x \n",  lk_buffer[0]);
		if(lk_buffer[0] != 15)
		{
			running = 0;
		}
		
		fprintf(stderr, "**********Press any button to stop.***********\n");
		
		nanosleep(&ts, NULL);

	}

	lk_exit();
	
	return ret;
	
}