#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab smarttab fenc=utf-8:
#
# libharu pdf library wrapper for python -- libharu.py
#

import os, sys
from ctypes import *
sys.path.append('./haru/lib')
os.environ["PATH"] = os.environ.get("PATH") + ":" + os.getcwd() + "/haru/lib"

from haru import *
from haru.c_func import *
from haru.hpdf_errorcode import *


class LibHaru():

    def __init__(self): 
        self.__pdf		= NULL
        self.nowPage	= 0
        self.pages		= []
        self.__x		= 595
        self.__y		= 847
        pass

    @HPDF_Error_Handler(None, HPDF_UINT, HPDF_UINT, c_void_p)
    def __error_handler (error_no, detail_no, user_data):
        printf ("ERROR: %s, detail_no=%u\n", error_detail[error_no], detail_no)
        sys.exit(1)

    def open(cls,paper=NULL, direction=HPDF_PAGE_PORTRAIT):

        cls.__pdf = HPDF_New (cls.__error_handler, NULL)
        if (not cls.__pdf):
            printf ("error: cannot create PdfDoc object\n")
            return 1

        if (not paper):
            paper		= HPDF_PAGE_SIZE_A4
            cls.__x	= 595
            cls.__y	= 847

        cls.addPage().page_setsize(paper, direction)
        return cls

    def page_setsize(cls, paper, direction):
        HPDF_Page_SetSize (cls.getPage(), paper, direction)
        HPDF_SetPageMode (cls.getPage(), HPDF_PAGE_MODE_FULL_SCREEN)
        return cls

    def addPage(cls):
        cls.pages.append(HPDF_AddPage(cls.__pdf))
        cls.nowPage	= len(cls.pages)
        return cls

    def mbEnable(cls, locate):
        if locate == 'JP':
            # JPEncoding
            HPDF_UseJPEncodings(cls.__pdf)
            HPDF_UseJPFonts (cls.__pdf)
        return cls

    def save(cls, fname):
        # save the document to a file
        HPDF_SaveToFile (cls.__pdf, fname)
        return cls

    def putStream(cls, toDest):
        HPDF_SaveToStream(cls.__pdf, toDest, HPDF_GetStreamSize(cls.__pdf))
        return cls

    def getPage(cls): return cls.pages[cls.nowPage - 1]
    def getPdf(cls): return cls.__pdf
    def getX(cls): return cls.__x
    def getY(cls): return cls.__y

    def close(cls):
        HPDF_Free(cls.__pdf)

class SuperHaruObject():
    __haru = NULL

    def __init__(cls, haru): cls.__haru = haru 
    def page(cls): return cls.__haru.getPage()
    def pdf(cls): return cls.__haru.getPdf()
    def x(cls): return cls.__haru.getX()
    def y(cls): return cls.__haru.getY()

class HaruDraw(SuperHaruObject):

    def __init__(cls, haru):
        SuperHaruObject.__init__(cls, haru)
        pass

    def rect_with_fill(cls, pos_x, pos_y, width, height, color):
        # Draw Rectangle
        HPDF_Page_SetDash (cls.page(), NULL, 0, 0)
        HPDF_Page_SetRGBFill (cls.page(), color[0], color[1], color[2])
        HPDF_Page_Rectangle(cls.page(), pos_x, cls.y() - (pos_y + height) , width, height)
        HPDF_Page_Fill (cls.page())

    def line(cls, pos_x, pos_y, length, point, color):
        page = cls.page()
        HPDF_Page_SetDash (page, NULL, 0, 0)
        HPDF_Page_SetLineWidth (page, point)
        HPDF_Page_SetRGBStroke (page, color[0], color[1], color[2])
        HPDF_Page_MoveTo (page, pos_x, cls.y() - pos_y)
        HPDF_Page_LineTo (page, pos_x + length, cls.y() - pos_y)
        HPDF_Page_Stroke (page)
        return cls

    def vline(cls, pos_x, pos_y, length, point, color):
        page = cls.page()
        HPDF_Page_SetDash (page, NULL, 0, 0)
        HPDF_Page_SetLineWidth (page, point)
        HPDF_Page_SetRGBStroke (page, color[0], color[1], color[2])
        HPDF_Page_MoveTo (page, pos_x, cls.y() - pos_y)
        HPDF_Page_LineTo (page, pos_x, cls.y() - pos_y + length)
        HPDF_Page_Stroke (page)
        return cls

    def dash_line(cls, pos_x, pos_y, length, point, dash, color):
        page = cls.page()
        HPDF_Page_SetDash (page, dash, 1, 1)
        HPDF_Page_SetLineWidth (page, point)
        HPDF_Page_SetRGBStroke (page, color[0], color[1], color[2])
        HPDF_Page_MoveTo (page, pos_x, cls.y() - pos_y)
        HPDF_Page_LineTo (page, pos_x + length, cls.y() - pos_y)
        HPDF_Page_Stroke (page)
        return cls

    def rect(cls, pos_x, pos_y, width, height, point, color):
        page = cls.page()
        HPDF_Page_SetDash (page, NULL, 0, 0)
        HPDF_Page_SetLineWidth (page, point)
        HPDF_Page_SetRGBStroke (page, color[0], color[1], color[2])
        HPDF_Page_Rectangle(page, pos_x, cls.y() - (pos_y + height), width, height)
        HPDF_Page_Stroke (page)
        return cls

class HaruText(SuperHaruObject):

    __HaruEnc = { 'EUC-JP':'EUC-H', 'SJIS':'90ms-RKSJ-H'}

    def __init__(cls, haru, Encoding="EUC-JP"):
        SuperHaruObject.__init__(cls, haru)
        cls.__Encoding = Encoding
        cls.__font		= NULL
        cls.__text		= []
        cls.__size      = 0
        pass

    def open_font(cls, fname):
        __pdf		= cls.pdf()
        font_name	= HPDF_LoadTTFontFromFile (__pdf, fname, HPDF_TRUE);
        cls.__font	= HPDF_GetFont (__pdf, font_name, cls.get_haru_encode())
        return cls

    def set_style(cls, size, color): 
        cls.__size  = size
        HPDF_Page_SetFontAndSize (cls.page(), cls.__font, size)
        HPDF_Page_SetRGBFill (cls.page(), color[0], color[1], color[2])
        return cls

    def put_with_width(cls, text):
        cls.put(text)
        return HPDF_Page_TextWidth(cls.page(), ''.join(cls.__text))

    ### 2016/11/10 support multi line text
    def put(cls, text):
        strArry = text.encode("utf-8").strip().split("\n")
        if len(strArry) > 1:
            for st in strArry:
                cls.__text.extend([ unicode(st, "utf-8").encode(cls.get_encode()), "\n"])
                ###cls.__text.extend([ unicode(st, "utf-8"), "\n"])
        else:
            cls.__text.append(text.encode(cls.get_encode()))
            ### 本来は↓こっちであるべき（だと思う）が何故かフォントの文字位置？の
            ### 判定がアスキー文字系だけ狂ってしまう為テンプレート化修正の際に修正
            #cls.__text.append(text if isinstance(text, unicode) else unicode(text,"utf-8"))
        return cls

    def setAutoReduce(cls, size):
        char_w = HPDF_Page_TextWidth(cls.page(), ''.join(cls.__text))

        while (char_w > size):
            w = HPDF_Page_GetCurrentFontSize(cls.page())
            HPDF_Page_SetFontAndSize (cls.page(), cls.__font, (w-1))
            char_w = HPDF_Page_TextWidth(cls.page(), ''.join(cls.__text))
        print char_w
        return cls

    def write_with_align(cls, pos, width, x, y, _indent = 0):
        char_w = HPDF_Page_TextWidth(cls.page(), ''.join(cls.__text))
        if pos in ["center","CENTER"]:
            cls.write(x + (width - char_w) / 2, y)	
        elif pos in ["right", "RIGHT"]:
            cls.write(x + width - char_w - _indent, y)	
        return cls

    ### 2016/11/10 support multi line text
    def write(cls, pos_x, pos_y):
        HPDF_Page_BeginText (cls.page())
        HPDF_Page_MoveTextPos(cls.page(), pos_x, cls.y() - pos_y)
        HPDF_Page_SetTextLeading(cls.page(), cls.__size);
        for st in cls.__text:
            if st == "\n":
                HPDF_Page_MoveToNextLine(cls.page())
            else:
                HPDF_Page_ShowText(cls.page(), ''.join(st))
                ### 本来は↓こっちであるべき（だと思う）が何故かフォントの文字位置？の
                ### 判定がアスキー文字系だけ狂ってしまう為テンプレート化修正の際に修正
                ##HPDF_Page_ShowText(cls.page(), ''.join(st.encode(cls.get_encode())))
        HPDF_Page_EndText (cls.page())
        return cls

    def flush(cls): cls.__text	= []
    def get_haru_encode(cls): return cls.__HaruEnc[cls.__Encoding]		
    def get_encode(cls): return cls.__Encoding
    def getFontHeight(cls):
        height_as  = int(HPDF_Font_GetAscent(cls.__font))
        height_ds  = int(HPDF_Font_GetDescent(cls.__font))
        return round(float(height_as + height_ds) / 72, 1)

class HaruImage(SuperHaruObject):

    def __init__(cls, haru):
        SuperHaruObject.__init__(cls, haru)
        pass

    def put_image(cls, fname, x, y, width, height):
        __pdf	= cls.pdf()
        image	= HPDF_LoadPngImageFromFile (__pdf, fname)

        HPDF_Page_DrawImage (cls.page(), image, x, y, width, height)
        return cls

