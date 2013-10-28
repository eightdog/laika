/*
 * example_3.c:
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
#include <stdlib.h>
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
	//struct timespec ts;
	unsigned char adc_convert_1;
	unsigned char adc_convert_2;
	unsigned char button_state;
	
	lk_init();
	
	running = 1;
	//ts.tv_nsec = 500000000;
	
	ret = exp_dout_all(MODULE_ONE, 0, lk_buffer);
	

	
	while(running)
	{

		system("clear");
		
		ret = exp_ain(MODULE_ONE, lk_buffer);
		display_return_code(ret);
		
		adc_convert_1 = (char)(lk_buffer[0] / 4);
		adc_convert_2 = (char)(lk_buffer[1] / 4);
		fprintf(stderr, "MOTOR Speed 0: %x \n",  adc_convert_1);
		fprintf(stderr, "MOTOR Speed 1: %x \n",  adc_convert_2);
		
		ret = exp_din(MODULE_ONE, lk_buffer);
		button_state = lk_buffer[0];
		fprintf(stderr, "Button Value: %x \n",  button_state);
		
		if(!(button_state & EXP_BUTTON_0_MASK))
		{
			ret = exp_motors(MODULE_ONE, EXP_MOTOR_1, EXP_MOTOR_FORWARD, adc_convert_1, lk_buffer);
			ret = exp_dout_x(MODULE_ONE, EXP_OUT_0, 1, lk_buffer);
			display_return_code(ret);
		}
		else
		{
			ret = exp_motors(MODULE_ONE, EXP_MOTOR_1, EXP_MOTOR_STOP, adc_convert_1, lk_buffer);
			ret = exp_dout_x(MODULE_ONE, EXP_OUT_0, 0, lk_buffer);
			display_return_code(ret);
		}
		if(!(button_state & EXP_BUTTON_1_MASK))
		{
			ret = exp_motors(MODULE_ONE, EXP_MOTOR_2, EXP_MOTOR_FORWARD, adc_convert_2, lk_buffer);
			ret = exp_dout_x(MODULE_ONE, EXP_OUT_1, 1, lk_buffer);
			display_return_code(ret);
		}
		else
		{
			ret = exp_motors(MODULE_ONE, EXP_MOTOR_2, EXP_MOTOR_STOP, adc_convert_2, lk_buffer);
			ret = exp_dout_x(MODULE_ONE, EXP_OUT_1, 0, lk_buffer);
			display_return_code(ret);
		}
		
		if(!(button_state & EXP_BUTTON_2_MASK))
		{
			running = 0;
		}
		
		fprintf(stderr, "**********Press Button 2 to stop.***********\n");
		
		//nanosleep(&ts, NULL);

	}

	lk_exit();
	
	return ret;
	
}