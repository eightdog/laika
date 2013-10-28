/*
 * laika.h:
 *	Top-level Laika interface module
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
 
#ifndef LAIKA_H
#define LAIKA_H

#include "exp.h"
#include "luna.h"

#define ON 1
#define OFF 0
#define SYNC_BYTE 0x55
#define MODULE_ID_MASK 0b00000011
#define LK_BUFFER_SIZE 32

#define WRITE_ONE_BYTE 		0x02							//Write one byte
#define WRITE_TWO_BYTES 	0x04							//Write two bytes
#define WRITE_THREE_BYTES 	0x06							//Write three bytes
#define WRITE_FOUR_BYTES 	0x08							//Write four bytes
#define WRITE_FIVE_BYTES 	0x0A							//Write five bytes
#define READ_ONE_BYTE 		0x03							//Read one byte
#define READ_TWO_BYTES 		0x05							//Read two bytes
#define READ_THREE_BYTES 	0x07							//Read three bytes
#define READ_FOUR_BYTES 	0x09							//Read four bytes
#define READ_FIVE_BYTES 	0x0B							//Read five bytes

enum module_number{MODULE_ONE, MODULE_TWO, MODULE_THREE, MODULE_FOUR};

//function prototypes
int lk_init(void);
int lk_exit(void);

#endif