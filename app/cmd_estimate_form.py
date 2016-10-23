#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# libharu test -- haru_demo.py
#

import os, sys
from ctypes import *
from libharu import *
import logging

def main():

	haru	= LibHaru()
	haru.open().page_setsize(HPDF_PAGE_SIZE_A4, HPDF_PAGE_PORTRAIT).mbEnable('JP')

	draw		= HaruDraw(haru)
	text		= HaruText(haru)
	font_dir	= os.path.dirname(os.path.realpath(__file__)) + "/../font/"

	## Header draw
	draw.rect_with_fill(25, 27, 545, 25, [0.28, 0.28, 0.28])
	text.open_font(font_dir + "GenShinGothic-P-Heavy.ttf").set_style(16,[1,1,1])
	text.put(u'御　請　求　書').write_with_align("center", 0, 47).flush()

	## invoice meta infomation
	PROJECT_NO	= u'PRINV1000048001'
	CREATE_DATE	= u'2015年7月30日'
	INVOICE_NO	= u'1'

	text.open_font(font_dir + "GenShinGothic-P-Regular.ttf").set_style(9.5,[0.25,0.25,0.25])
	text.put(u'請求No：').write(haru.getX() - 160, 65).flush()
	text.put(PROJECT_NO).write(haru.getX() - 115, 65).flush()

	text.put(u'作成日：').write(haru.getX() - 156, 78).flush()
	text.put(CREATE_DATE).write(haru.getX() - 115, 78).flush()

	text.put(u'請求番：').write(haru.getX() - 156, 91).flush()
	text.put(INVOICE_NO).write(haru.getX() - 115, 91).flush()

	## destination draw
	DISTINATION	= u'ＡＲアドバンストテクノロジー株式会社'
	text.set_style(13,[0.25,0.25,0.25])
	text.put(DISTINATION).write(27, 111).flush()

	text.set_style(12,[0.25,0.25,0.25])
	text.put(u'様').write(248, 111).flush()
	draw.line(25, 115, 240, 1, [0.27, 0.27, 0.27])

	## company information draw 
	COMPANY_NAME	= u'株式会社Grrow'
	POST_NO			= u'〒140-001'
	ADRESS_1		= u'東京都品川区北品川'
	ADRESS_2		= u'1-9-7 トップルーム品川1015'
	PHONE_NO		= u'TEL：090-2420-2989'

	text.open_font(font_dir + "GenShinGothic-P-Bold.ttf").set_style(12,[0.25,0.25,0.25])
	text.put(COMPANY_NAME).write(haru.getX() - 178, 145).flush()

	text.open_font(font_dir + "GenShinGothic-P-Regular.ttf").set_style(11,[0.25,0.25,0.25])
	text.put(ADRESS_1).write(haru.getX() - 132, 166).flush()
	text.put(ADRESS_2).write(haru.getX() - 166, 179).flush()

	text.set_style(9.5,[0.25,0.25,0.25])
	text.put(POST_NO).write_with_align("right", 135, 166).flush()
	text.put(PHONE_NO).write_with_align("right", 33, 192).flush()
	
	## greeting message field
	MESSAGE1	= u'下記の通りお見積り致しますので、'
	MESSAGE2	= u'よろしくお願い申し上げます。'

	text.set_style(10.5,[0.2,0.2,0.2])
	text.put(MESSAGE1).write(29, 145).flush()
	text.put(MESSAGE2).write(29, 158).flush()

	## invoice infomation
	draw.line(25, 186, 290, 1, [0.27, 0.27, 0.27])
	draw.line(25, 204, 290, 1, [0.27, 0.27, 0.27])
	draw.line(25, 222, 290, 1, [0.27, 0.27, 0.27])
	draw.line(25, 240, 290, 1, [0.27, 0.27, 0.27])

	text.set_style(9,[0.25,0.25,0.25])
	text.put(u'件 　 名 　 　 ：').write(25, 182).flush()
	text.put(u'納 入 期 限 　 ：').write(25, 198).flush()
	text.put(u'納 入 方 式 　 ：').write(25, 216).flush()
	text.put(u'御 支 払 条 件 ：').write(25, 234).flush()


	haru.save('/vagrant_data/demo.pdf')
	haru.close()

	return 0

if HPDF_NOPNGLIB:
    printf("WARNING: if you want to run this demo, \n"
           "make libhpdf with HPDF_USE_PNGLIB option.\n")
    sys.exit(1)
else:
    main()
