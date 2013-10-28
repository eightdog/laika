/*
 * exp.h:
 *	Interface to Laika Explorer hardware module
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
 
#ifndef EXP_H
#define EXP_H

#define EXP_ID 0b01000100
#define EXP_BUTTON_0_MASK 0b00000001 
#define EXP_BUTTON_1_MASK 0b00000010 
#define EXP_BUTTON_2_MASK 0b00000100 
#define EXP_BUTTON_3_MASK 0b00001000 
#define EXP_MOTOR_1 1
#define EXP_MOTOR_2 2
#define EXP_MOTOR_STOP 0
#define EXP_MOTOR_FORWARD 1
#define EXP_MOTOR_REVERSE 2
#define EXP_MOTOR_BRAKE 3
#define EXP_OUT_0 0
#define EXP_OUT_1 1
#define EXP_OUT_2 2
#define EXP_OUT_3 3
#define EXP_OUT_4 4
#define EXP_OUT_5 5
#define EXP_OUT_6 6

enum{EXP_DOUT_ALL=2, EXP_DOUT_X, EXP_DIN, EXP_AIN, EXP_MOTORS};

//function prototypes
unsigned char exp_dout_all(unsigned char module_id_lower_two_bits, unsigned char data_in, unsigned int* buffer_in);
unsigned char exp_dout_x(unsigned char module_id_lower_two_bits, unsigned char pin_in, unsigned char data_in, unsigned int* buffer_in);
unsigned char exp_din(unsigned char module_id_lower_two_bits, unsigned int* buffer_in);
unsigned char exp_ain(unsigned char module_id_lower_two_bits, unsigned int* buffer_in);
unsigned char exp_motors(unsigned char module_id_lower_two_bits, unsigned char motor_in, unsigned char direction_in, unsigned char speed_in , unsigned int* buffer_in);

#endif

