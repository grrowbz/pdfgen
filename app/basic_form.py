#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#

import os, sys
from ctypes import *
from libharu import *

class BasicForm(object):

    haru		= ""
    text		= ""
    draw		= ""
    font		= ""

    def __init__(self, haru):

        self.haru	= haru
        self.haru.open().page_setsize(HPDF_PAGE_SIZE_A4, HPDF_PAGE_PORTRAIT).mbEnable('JP')

        self.draw	= HaruDraw(self.haru)
        self.text	= HaruText(self.haru)
        font_dir	= os.path.dirname(os.path.realpath(__file__)) + "/../font/"

        self.font = {	"Heavy" : font_dir + "GenShinGothic-P-Heavy.ttf",
                        "Regular" : font_dir +"GenShinGothic-P-Regular.ttf",
                        "Bold" : font_dir + "GenShinGothic-P-Bold.ttf"}
        ## Header 
        self.draw.rect_with_fill(25, 27, 545, 25, [0.28, 0.28, 0.28])

        ## invoice meta information
        self.setFont("Regular", 9.5, [0.25,0.25,0.25])
        self.text.put(u'作成日：').write(self.haru.getX() - 156, 78).flush()

        self.draw.line(25, 115, 240, 1, [0.27, 0.27, 0.27])

        ## project infomation
        self.setFont("Regular",9,[0.25,0.25,0.25])
        self.draw.line(25, 186, 290, 1, [0.27, 0.27, 0.27])
        self.text.put(u'件 　 名 　 　 ：').write(25, 182).flush()

        self.draw.line(25, 280, 290, 1, [0.27, 0.27, 0.27])
        self.draw.line(25, 282, 290, 1, [0.27, 0.27, 0.27])

        BoxY = 302
        BoxHeight = 318
        ### Item title box
        self.setFont("Regular",9,[0.25,0.25,0.25])
        self.draw.rect(25, BoxY, 540, 12, 1, [0.27, 0.27, 0.27])
        self.draw.rect(25, BoxY + 12, 540, BoxHeight, 1, [0.27, 0.27, 0.27])

        self.text.put(u'No').write(32, 312).flush()
        self.text.put(u'品名及び明細').write(168, 312).flush()
        self.text.put(u'数量').write(346, 312).flush()
        self.text.put(u'単位').write(388, 312).flush()
        self.text.put(u'単価').write(438, 312).flush()
        self.text.put(u'金額').write(515, 312).flush()

        ItemBoxHeight = BoxHeight + 10
        ### Item List Box
        self.draw.rect(25, BoxY, 25, ItemBoxHeight, 1, [0.27, 0.27, 0.27])
        self.draw.rect(50, BoxY, 280, ItemBoxHeight, 1, [0.27, 0.27, 0.27])
        self.draw.rect(330, BoxY, 50, ItemBoxHeight, 1, [0.27, 0.27, 0.27])
        self.draw.rect(380, BoxY, 35, ItemBoxHeight, 1, [0.27, 0.27, 0.27])
        self.draw.rect(415, BoxY, 65, ItemBoxHeight, 1, [0.27, 0.27, 0.27])
        self.draw.rect(480, BoxY, 85, ItemBoxHeight, 1, [0.27, 0.27, 0.27])

        InfoBoxY  = 630
        BottomBoxHeight = 70
        ### 納品物
        self.setFont("Regular",10,[0.25,0.25,0.25])
        self.text.put(u'納品物').write(32, InfoBoxY + 38).flush()
        self.draw.rect(25, InfoBoxY, 45, BottomBoxHeight - 2, 1, [0.27, 0.27, 0.27])
        self.draw.rect(70, InfoBoxY, 235, BottomBoxHeight - 2, 1, [0.27, 0.27, 0.27])

        ### Price Box
        self.setFont("Regular",11,[0.25,0.25,0.25])
        self.text.put(u'小計').write(480 - 26, InfoBoxY + 16).flush()
        self.text.put(u'消費税').write(480 - 39, InfoBoxY + 38).flush()
        self.setFont("Regular",12,[0.25,0.25,0.25])
        self.text.put(u'合計').write(480 - 26, InfoBoxY + 62).flush()

        self.draw.rect(480, InfoBoxY, 85, BottomBoxHeight - 2, 1, [0.27, 0.27, 0.27])
        self.draw.line(305, InfoBoxY, 175, 1, [0.27, 0.27, 0.27])
        self.draw.line(305, InfoBoxY + 22, 260, 1, [0.27, 0.27, 0.27])
        self.draw.line(305, InfoBoxY + 46, 260, 1, [0.27, 0.27, 0.27])
        self.draw.line(305, InfoBoxY + 68, 175, 1, [0.27, 0.27, 0.27])

        ### 備考
        self.draw.rect(25, 715, 540, 100, 1, [0.27, 0.27, 0.27])

        ItemBoxY = BoxY + 12
        for var in range(1, 21):
            self.draw.dash_line(25, ItemBoxY + 15 * var, 540, 0.7, [2, 1], [0.3, 0.3, 0.3])

    def setCompanyInfo(cls):
        ## company information
        KABU            = u'株式会社'
        COMPANY_NAME	= u'Grrow'
        POST_NO			= u'〒140-001'
        ADRESS_1		= u'東京都品川区北品川'
        ADRESS_2		= u'1-9-7 トップルーム品川1015'
        PHONE_NO		= u'TEL：090-2420-2989'

        cls.text.open_font(cls.font["Bold"]).set_style(16,[0.25,0.25,0.25])
        cls.text.put(KABU).write(cls.haru.getX() - 192, 149).flush()
        cls.text.open_font(cls.font["Bold"]).set_style(19,[0.25,0.25,0.25])
        cls.text.put(COMPANY_NAME).write(cls.haru.getX() - 126, 149).flush()

        cls.text.open_font(cls.font["Regular"]).set_style(11,[0.25,0.25,0.25])
        cls.text.put(ADRESS_1).write(cls.haru.getX() - 132, 166).flush()
        cls.text.put(ADRESS_2).write(cls.haru.getX() - 166, 179).flush()

        cls.setFont("Regular", 9.5,[0.25,0.25,0.25])
        ## 郵便番号の出力位置表示 画面サイズX幅 - 132 - 45
        cls.text.put(POST_NO).write_with_align("right", 45, cls.haru.getX() - 177, 166, 3).flush()
        ## 電話番号の設定
        cls.text.put(PHONE_NO).write_with_align("right", 133, cls.haru.getX() - 166, 192).flush()

    def setSignBox(cls):
        ### Sign Box
        cls.setFont("Regular",9,[0.25,0.25,0.25])
        cls.text.put(u'承認').write(433, 225).flush()
        cls.text.put(u'担当者').write(508, 225).flush()
        cls.draw.line(400, 230, 160, 1, [0.27, 0.27, 0.27])
        cls.draw.rect(400, 214, 80, 76, 1, [0.27, 0.27, 0.27])
        cls.draw.rect(480, 214, 80, 76, 1, [0.27, 0.27, 0.27])

    ## Font Setting method 
    def setFont(cls, name, weight, color):
        cls.text.open_font(cls.font[name]).set_style(weight,color)

    def setCreateDate(cls, date):
        cls.setFont("Regular",9.5,[0.25,0.25,0.25])
        cls.text.put(date).write(cls.haru.getX() - 115, 78).flush()

    ### client name set method
    def setClientName(cls, client_name):
        cls.setFont("Regular", 12,[0.25,0.25,0.25])
        cls.text.put(u'様').write(248, 111).flush()
        cls.text.put(client_name).setAutoReduce(215).write(27, 111).flush()

    ## project name set method
    def setTitle(cls, title):
        cls.setFont("Regular", 9,[0.25,0.25,0.25])
        cls.text.put(title).write(25 + 65, 182).flush()

    def setPrice(cls, title, price):
        subtotal    = int(price)
        tax         = int(round(subtotal * 0.08))
        price       = subtotal + tax

        cls.setFont("Regular",10,[0.25,0.25,0.25])
        textObj = cls.text.put(u"￥" + "{:,}".format(subtotal))
        textObj.write_with_align('right', 85, 480, 646, 3 ).flush()

        textObj = cls.text.put(u"￥" + "{:,}".format(tax))
        textObj.write_with_align('right', 85, 480, 668, 3 ).flush()

        textObj = cls.text.put(u"￥" + "{:,}".format(price))
        textObj.write_with_align('right', 85, 480, 692, 3 ).flush()

        cls.setFont("Regular",13,[0.25,0.25,0.25])
        cls.text.put(title).write(25, 276).flush()

        cls.setFont("Regular",15,[0.25,0.25,0.25])
        textObj = cls.text.put(u"￥" + "{:,}".format(int(price)))
        textObj.write_with_align('right', 166, 150, 276, 3 ).flush()

    def setDeliverables(cls, deliverables, num=1):
        cls.setFont("Regular",8.5,[0.25,0.25,0.25])
        cls.text.put(deliverables).write(75, 633 + (12 * num)).flush()

    def setRemarksColumn(cls, remarks, num=1):
        cls.setFont("Regular",8.5,[0.25,0.25,0.25])
        cls.text.put(remarks).write(30, 718 + (12 * num)).flush()

    def __align(cls, string, x, width, position):
        print len(string)
        #return (x + width) - len(string)

    def setItemData(cls, LineNo, no, item, qty, unit, uprice, price):
        cls.setFont("Regular",8.5,[0.25,0.25,0.25])
        YPos = 314 + (15 * LineNo) - 3

        cls.text.put(str(no)).write_with_align('center', 25, 25, YPos).flush()
        cls.text.put(unicode(item)).write(50 + 3, YPos).flush()
        cls.text.put(str(qty)).write_with_align('center', 50, 330, YPos).flush()
        cls.text.put(unicode(unit)).write_with_align('center', 35, 380, YPos).flush()

        if (int(uprice) < 0) :
            cls.setFont("Regular",8.5,[1,0,0])
        textObj = cls.text.put(u"￥" + "{:,}".format(int(uprice)))
        textObj.write_with_align('right', 65, 415, YPos, 3 ).flush()
        cls.setFont("Regular",8.5,[0.25,0.25,0.25])

        if (int(uprice) < 0) :
            cls.setFont("Regular",8.5,[1,0,0])
        textObj = cls.text.put(u"￥" + "{:,}".format(int(price)))
        textObj.write_with_align('right', 85, 480, YPos, 3).flush()
        cls.setFont("Regular",8.5,[0.25,0.25,0.25])

    def setItemDataForOnlySubTitle(cls, LineNo, no, item):
        cls.setFont("Regular",8.5,[0.25,0.25,0.25])
        ListPosition = 314 + (15 * LineNo) - 3
        cls.text.put(unicode(no)).write(25 + 10, ListPosition).flush()
        cls.text.put(unicode(item)).write(50 + 3, ListPosition).flush()

    def createObject(cls):
        return cls.haru

