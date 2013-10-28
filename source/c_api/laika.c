/*
 * laika.c:
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
 
#include <stdio.h>
#include <unistd.h>
#include <ftdi.h>
#include "include/laika/laika.h"

struct ftdi_context ftdic;
int ret;

int lk_init(void)
{

    if (ftdi_init(&ftdic) < 0)
    {
        fprintf(stderr, "ftdi_init failed\n");
        return EXIT_FAILURE;
    }

    if ((ret = ftdi_usb_open(&ftdic, 0x0403, 0x6015)) < 0)
    {
        fprintf(stderr, "unable to open ftdi device: %d (%s)\n", ret, ftdi_get_error_string(&ftdic));
        return EXIT_FAILURE;
    }

    if ((ret = ftdi_set_baudrate(&ftdic, 125000)) < 0)
    {
        fprintf(stderr, "Unable to set baudrate: %d (%s)\n", ret, ftdi_get_error_string(&ftdic));
        return EXIT_FAILURE;
    }

    if ((ret = ftdi_set_line_property2(&ftdic, BITS_8, STOP_BIT_1, NONE, BREAK_OFF)) < 0)
    {
        fprintf(stderr, "Unable to set 7O1: %d (%s)\n", ret, ftdi_get_error_string(&ftdic));
        return EXIT_FAILURE;
    }
	
	if ((ret = ftdi_setflowctrl(&ftdic, SIO_DISABLE_FLOW_CTRL)) < 0)
    {
        fprintf(stderr, "Unable to set flow: %d (%s)\n", ret, ftdi_get_error_string(&ftdic));
        return EXIT_FAILURE;
    }
	
	ftdic.usb_read_timeout = 5000;
	
	return EXIT_SUCCESS;
}

int lk_exit(void)
{
    if ((ret = ftdi_usb_close(&ftdic)) < 0)
    {
        fprintf(stderr, "unable to close ftdi device: %d (%s)\n", ret, ftdi_get_error_string(&ftdic));
        return EXIT_FAILURE;
    }

    ftdi_deinit(&ftdic);
    return EXIT_SUCCESS;
}







