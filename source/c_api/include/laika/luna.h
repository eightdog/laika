/*
 * luna.h:
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
#ifndef LUNA_H
#define LUNA_H

#define LUNA_ID 0b01001100

enum{LUNA_OUTPUT_SET=2, LUNA_CURRENT_READ};

unsigned char luna_output(unsigned char module_id_lower_two_bits, unsigned char output_state_1, unsigned char output_state_2, unsigned int* buffer_in);

#endif

