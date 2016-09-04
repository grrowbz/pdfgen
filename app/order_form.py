#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# libharu test -- haru_demo.py
#

import os, sys
from ctypes import *
from libharu import *

def main():

	haru	= LibHaru()
	haru.open().page_setsize(HPDF_PAGE_SIZE_A4, HPDF_PAGE_PORTRAIT).mbEnable('JP')

	draw	= HaruDraw(haru)
	text	= HaruText(haru)

	## Header draw
	## draw.rect_with_fill( x, y, width, height, color)
	draw.rect_with_fill(25, 27, 545, 25, [0.28, 0.28, 0.28])
	text.open_font("./font_1_ant-kaku.ttf").set_style(16,[1,1,1])
	text.put(u'御　請　求　書').write_with_align("center", 0, 47).flush()

	## invoice meta infomation
	CREATE_DATE	= u'2016年1月31日'
	INVOICE_NO	= u'28'
	PROJECT_NO	= u'PRINV1000034' + u'{:03}'.format(int(INVOICE_NO))

	text.set_style(9.5,[0.25,0.25,0.25])
	text.put(u'請求No：').write(435, 65).flush()
	text.put(PROJECT_NO).write(480,  65).flush()

	text.put(u'作成日：').write(haru.getX() - 156, 78).flush()
	text.put(CREATE_DATE).write(haru.getX() - 115, 78).flush()

	text.put(u'請求番：').write(haru.getX() - 156, 91).flush()
	text.put(INVOICE_NO).write(haru.getX() - 115, 91).flush()

	## destination draw
	DISTINATION	= u'アルカディア・システムズ 株式会社'
	text.set_style(13,[0.25,0.25,0.25])
	text.put(DISTINATION).write(27, 111).flush()

	text.set_style(12,[0.25,0.25,0.25])
	text.put(u'様').write(248, 111).flush()
	draw.line(25, 115, 240, 1, [0.27, 0.27, 0.27])

	## company information draw 
	#COMPANY_NAME	= u'株式会社Grrow'
	#POST_NO		= u'〒140-001'
	#ADRESS_1		= u'東京都品川区北品川'
	#ADRESS_2		= u'1-9-7 トップルーム品川1015'
	#PHONE_NO		= u'TEL：090-2420-2989'

	Info = { 'COMPANY_NAME' : u'光部システム・コンサルティング',
			'POST_NO' : u'〒131-0046',
			'ADDRESS_1' : u'東京都墨田区京島',
			'ADDRESS_2' : u'1-29-6',
			'PHONE_NO' : u'TEL：090-2420-2989' }

	text.set_style(12,[0.25,0.25,0.25])
	text.put(Info['COMPANY_NAME']).write_with_align("right", -30, 145).flush()

	text.set_style(11,[0.25,0.25,0.25])
	size	= text.put_with_width(Info['ADDRESS_1'])
	text.write(haru.getX() - size - 25 - 5, 166).flush()
	text.put(Info['ADDRESS_2']).write_with_align("right", -30, 179).flush()

	text.set_style(10.5,[0.25,0.25,0.25])
	text.put(Info['POST_NO']).write_with_align("right", -35 - size, 166).flush()
	text.put(Info['PHONE_NO']).write_with_align("right", -30, 192).flush()

	## greeting message field
	MESSAGE1	= u'下記の通りご請求申し上げます。'
	MESSAGE2	= u'記載の銀行口座へお振り込み下さい。'

	text.set_style(11,[0.25,0.25,0.25])
	text.put(MESSAGE1).write(29, 240).flush()
	text.put(MESSAGE2).write(29, 253).flush()

	## invoice infomation
	draw.line(25, 186, 290, 1, [0.27, 0.27, 0.27])
	draw.line(25, 201, 290, 1, [0.27, 0.27, 0.27])

	text.set_style(9,[0.25,0.25,0.25])
	text.put(u'件 　 名 　：').write(25, 182).flush()
	text.put(u'支 払 期 限：').write(25, 198).flush()

	## bill information
	draw.line(25, 286, 290, 1, [0.27, 0.27, 0.27])
	draw.line(25, 288, 290, 1, [0.27, 0.27, 0.27])

	text.set_style(12,[0.25,0.25,0.25])
	text.put(u'御請求金額（税込）').write(27, 282).flush()
	
	## stamp space
	rect_w = 70 
	rect_h = 53
	draw.rect(haru.getX() - 25 - rect_w, 202, rect_w, 13, 1, [0.28, 0.28, 0.28])
	draw.rect(haru.getX() - 25 - rect_w * 2, 202, rect_w, 13, 1, [0.28, 0.28, 0.28])
	draw.rect(haru.getX() - 25 - rect_w, 215, rect_w, rect_h, 1, [0.28, 0.28, 0.28])
	draw.rect(haru.getX() - 25 - rect_w * 2, 215, rect_w, rect_h, 1, [0.28, 0.28, 0.28])

	text.set_style(9,[0.25,0.25,0.25])
	text.put(u'承認').write(haru.getX() - 25 - rect_w * 2 + (rect_w / 2 - 9), 213).flush()
	text.put(u'担当者').write(haru.getX() - 25 - rect_w + (rect_w / 2 - 13.5), 213).flush()

	image	= HaruImage(haru)
	image.put_image('./sign.png', 520, 590, 30, 30)
	image.put_image('./sign.png', 452, 591, 30, 30)

	#############################################################################
	## 品目エリアの生成
	line_range	= 23
	item_area	= 313
	rect_w		= haru.getX() - 50 
	rect_h		= item_area

	draw.rect(25, 300, rect_w, rect_h, 1, [0.28, 0.28, 0.28])
	draw.line(25, 314, rect_w, 1, [0.28, 0.28, 0.28])

	for num in range(0, line_range):
		draw.dash_line(25, 314 + 13 * num, rect_w, 0.2, [2], [0.8, 0.8, 0.8])

	p = [25, 20, 265, 50, 40, 70, 100]
	for num in range(1, 7):
		draw.rect(sum(p[:num]), 300, p[num], rect_h, 1, [0.28, 0.28, 0.28])

	## 品目エリアのヘッダーを生成
	text.set_style(9,[0.25,0.25,0.25])
	header_list 	= [ u'No.', u'品名及び明細', u'数量', u'単位', u'単価', u'金額']
	ct				= 1

	for txt in header_list:
		siz		= text.put_with_width(txt)
		text.write(sum(p[:ct]) + (p[ct] / 2 ) - (siz / 2), item_area - 2 ).flush()
		ct += 1

	for num in range(1, (line_range - 1)):
		siz		= text.put_with_width(str(num))
		text.write(sum(p[:2]) - siz - 2, 326 + 13 * num - 1).flush()

	#############################################################################
	rect_w	= haru.getX() - 50
	rect_h	= 82
	top_h	= item_area + (line_range * 13)

	## 品目エリアの下側と2重線を生成
	draw.rect(25, top_h + 1 , rect_w, rect_h, 1, [0.28, 0.28, 0.28])
	draw.line(25, top_h + 3, rect_w, 1, [0.28, 0.28, 0.28])

	## 小計以下の金額欄（右）とその欄の説明（左）の枠を生成
	draw.rect(sum(p[:6]), top_h + 3, rect_w - sum(p[:6]) + 25, 80, 1, [0.28, 0.28, 0.28])

	## 小計以下の行を生成
	for num in range(0, 4):
		draw.rect(sum(p[:3]), top_h + 3 + (num * 20), rect_w - sum(p[:3]) + 25, 20, 1, [0.28, 0.28, 0.28])

	## 品目エリアの下側の説明欄を生成
	text.set_style(11,[0.25,0.25,0.25])
	title_list 	= [ u'小計', u'消費税', u'源泉税及び復興特別所得税', u'合計']
	ct			= 1

	for txt in title_list:
		siz			= text.put_with_width(txt)
		text.write(sum(p[:6]) - siz - 3, top_h + 3 + ((ct - 1) * 20) + 14).flush()
		ct += 1
	#############################################################################
	rect_w	= haru.getX() - 50 
	rect_h	= 110
	abs_pos	= haru.getY() - 25 - rect_h

	BANK_INFO	= u'東京三菱UFJ銀行　新稲毛出張所　普通 0454407'
	DIST_NAME	= u'光部 智幸'
	ATTENTION1	= u'【ご注意事項】'
	ATTENTION2	= u'大変恐縮ですが、お振込み手数料は御社ご負担にてお願い致します。'

	draw.rect(25, abs_pos, rect_w, rect_h, 1, [0.28, 0.28, 0.28])

	text.set_style(10,[0.25,0.25,0.25])
	text.put(u'【お振込先金融機関】').write(28, abs_pos + 20).flush()
	text.put(BANK_INFO).write(36, abs_pos + 20 + 14).flush()
	text.put(DIST_NAME).write(36, abs_pos + 20 + (14 * 2)).flush()
	text.put(ATTENTION1).write(28, abs_pos + 20 + (14 * 4)).flush()
	text.put(ATTENTION2).write(36, abs_pos + 20 + (14 * 5)).flush()
	################################################################################

	PROJECT_TITLE	= u'技術支援事業に関する支援業務' + u'2016年度1月分'
	text.set_style(11,[0.25,0.25,0.25])
	text.put(PROJECT_TITLE).write(82, 182).flush()

	DUE_DATE		= u'2016年2月15日'
	text.set_style(9,[0.25,0.25,0.25])
	text.put(DUE_DATE).write(82, 198).flush()

	Item	= [{'title' : u'受託事業に関する営業活動支援業務', 'value' : 200000, 'num' : 1, 'unit' : u'式'}]
	ct		= 1
	total	= 0
	text.set_style(9.5,[0.25,0.25,0.25])
	for itm in Item:
		row_pos = 326 + 13 * ct - 1
		text.put(itm["title"]).write(sum(p[:2]) + 5 , row_pos).flush()
		text.put(str(itm["num"])).write(sum(p[:3]) + (p[3] / 2) , row_pos).flush()

		length	= text.put_with_width(itm["unit"])
		text.write(sum(p[:4]) + (p[4] / 2) - (length / 2), row_pos).flush()

		length	= text.put_with_width(u"￥{:,d}".format(itm["value"]))
		text.write(sum(p[:6]) - length - 3 , row_pos).flush()

		length	= text.put_with_width(u"￥{:,d}".format(itm["value"] * itm["num"]))
		text.write(sum(p[:7]) - length - 3 , row_pos).flush()
		total += itm["value"]	
		ct += 1

	row_pos	= top_h + 3 + 14
	size	= text.put_with_width(u"￥{:,d}".format(total))
	text.write(sum(p[:7]) - size - 3, row_pos).flush()

	size	= text.put_with_width(u"￥{:,d}".format(int(total * 0.08)))
	text.write(sum(p[:7]) - size - 3, row_pos + 20).flush()

	size	= text.put_with_width(u"￥{:,d}".format(int(total * 0.1021)))
	text.write(sum(p[:7]) - size - 3, row_pos + (2 * 20)).flush()

	size	= text.put_with_width(u"￥{:,d}".format(int(total * 1.08 - (total * 0.1021))))
	text.write(sum(p[:7]) - size - 3, row_pos + (3 * 20)).flush()

	text.set_style(13,[0.25,0.25,0.25])
	length	= text.put_with_width(u"￥{:,d}".format(int(total * 1.08 - (total * 0.1021))))
	text.write(290 - length + 15, 282).flush()

	haru.save('/vagrant_data/demo.pdf')
	haru.close()

	return 0

if HPDF_NOPNGLIB:
    printf("WARNING: if you want to run this demo, \n"
           "make libhpdf with HPDF_USE_PNGLIB option.\n")
    sys.exit(1)
else:
    main()
