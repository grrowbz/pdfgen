#!/bin/env python
# -*- coding: utf-8 -*-
###
## * << Haru Free PDF Library 2.0.0 >> -- line_demo.c
## *
## * Copyright (c) 1999-2006 Takeshi Kanno <takeshi_kanno@est.hi-ho.ne.jp>
## *
## * Permission to use, copy, modify, distribute and sell this software
## * and its documentation for any purpose is hereby granted without fee,
## * provided that the above copyright notice appear in all copies and
## * that both that copyright notice and this permission notice appear
## * in supporting documentation.
## * It is provided "as is" without express or implied warranty.
## *
##

## port to python by Li Jun
## http://groups.google.com/group/pythoncia

import os, sys

from ctypes import *

from haru import *
from haru.c_func import *
from haru.hpdf_errorcode import *


@HPDF_Error_Handler(None, HPDF_UINT, HPDF_UINT, c_void_p)
def error_handler (error_no, detail_no, user_data):
    global pdf
    printf ("ERROR: %s, detail_no=%u\n", error_detail[error_no],
                detail_no)
    HPDF_Free (pdf)
    sys.exit(1)

def draw_rect (page,  x, y, label):

    HPDF_Page_Rectangle(page, x, y - 40, 220, 25)

def main ():
    global pdf

    page_title = "Line Example"

    pdf = HPDF_New (error_handler, NULL)
    if (not pdf):
        printf ("error: cannot create PdfDoc object\n")
        return 1

    # create default-font
    font = HPDF_GetFont (pdf, "Helvetica", NULL)

    # add a new page object.
    page = HPDF_AddPage (pdf)

    HPDF_Page_SetFontAndSize (page, font, 10)

    # Draw Rectangle
    HPDF_Page_SetLineWidth (page, 2)
    HPDF_Page_SetRGBStroke (page, 0, 0, 0)
    HPDF_Page_SetRGBFill (page, 0.75, 0.0, 0.0)

    draw_rect (page, 300, 720, "Fill")
    HPDF_Page_Fill (page)

    # save the document to a file
    HPDF_SaveToFile (pdf, '/vagrant_data/demo2.pdf')

    # clean up
    HPDF_Free (pdf)

    return 0


main()
