#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# libharu test -- haru_demo.py
#

import os, sys

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, '../app/'))

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

def raw_handler(event, context):

    global pdf 
    pdf = HPDF_New (error_handler, NULL)
    if (not pdf):
        printf ("error: cannot create PdfDoc object\n")
        return 1

    # JPEncoding
    HPDF_UseJPEncodings (pdf)
    HPDF_UseJPFonts (pdf)

    # create default-font
    font = HPDF_GetFont (pdf, "Helvetica", NULL)

    # add a new page object.
    page = HPDF_AddPage (pdf)

    # A4 size
    HPDF_Page_SetSize (page, HPDF_PAGE_SIZE_A4, HPDF_PAGE_PORTRAIT)
    HPDF_SetPageMode (page, HPDF_PAGE_MODE_FULL_SCREEN)

    # 72dpi A4 size : width x height = 847 x 595
    page_x = 595
    page_y = 820

    HPDF_Page_SetFontAndSize (page, font, 10)

    # Draw Rectangle
    HPDF_Page_SetLineWidth (page, 2)
    HPDF_Page_SetRGBStroke (page, 0, 0, 0)
    HPDF_Page_SetRGBFill (page, 0.4, 0.4, 0.4)

    HPDF_Page_Rectangle(page, 25, page_y - 25, 545, 25)
    HPDF_Page_Fill (page)

    #### title text ####
    font_size	= 16 
    page_title	= u'Invoice'.encode('euc-jp')

    filename1="%s" % path + '/../assets/img/sign.png'
    print filename1

    image = HPDF_LoadPngImageFromFile (pdf, filename1)
    # Draw image to the canvas.
    
    HPDF_Page_DrawImage (page, image, 100, 300, HPDF_Image_GetWidth (image) / 20,
                                          HPDF_Image_GetHeight (image) / 20)

    HPDF_Page_SetRGBFill (page, 1, 1, 1)

    char_size	= HPDF_Page_TextWidth(page, page_title)

    HPDF_Page_BeginText (page)
    HPDF_Page_MoveTextPos(page, page_x / 2 - (char_size / 2), page_y - 20)
    HPDF_Page_ShowText (page, page_title)
    HPDF_Page_EndText (page)

    # save the document to a file
    HPDF_SaveToFile (pdf, '/tmp/.demo.pdf')
    with open('/tmp/.demo.pdf', 'r') as f:
        return f.read()
