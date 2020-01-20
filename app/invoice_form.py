#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# libharu test -- haru_demo.py
#

import os, sys
from app.basic_form import *
from app.libharu import *
from ctypes import *

class InvoiceForm(BasicForm):

    def __init__(self, haru):

        super(self.__class__, self).__init__(haru)

        ## Header 
        self.setFont("Heavy",16,[1,1,1])
        self.text.put(u'御　請　求　書').write_with_align("center", self.haru.getX(), 0, 47).flush()

        ## invoice meta information
        self.setFont("Regular",9.5,[0.25,0.25,0.25])
        self.text.put(u'請求No：').write(self.haru.getX() - 160, 65).flush()
        self.text.put(u'請求番：').write(self.haru.getX() - 156, 91).flush()

        ## greeting message field
        MESSAGE1	= u'下記の通り、ご請求申し上げます'
        MESSAGE2	= u'記載の銀行口座にてお振込み下さい。'

        self.text.set_style(10.5,[0.2,0.2,0.2])
        self.text.put(MESSAGE1).write(29, 230).flush()
        self.text.put(MESSAGE2).write(29, 243).flush()

        ## invoice infomation
        self.setFont("Regular", 9,[0.25,0.25,0.25])
        self.draw.line(25, 203, 290, 1, [0.27, 0.27, 0.27])
        self.text.put(u'支 払 期 限 　 ：').write(25, 199).flush()

        self.setCompanyInfo()
        self.setSignBox()

    def setRemarksColumn(cls, remarks):
        super(cls.__class__, cls).setRemarksColumn(u"【お振込先金融機関】")
        super(cls.__class__, cls).setRemarksColumn(u"　東京三菱UFJ銀行　麻布支店　0196203", 2)
        super(cls.__class__, cls).setRemarksColumn(u"　株式会社Grrow", 3)
        super(cls.__class__, cls).setRemarksColumn(remarks, 4)

    ## invoice meta infomation set methods 
    def setProjectNumber(cls, number, order):
        cls.setFont("Regular",9.5,[0.25,0.25,0.25])
        cls.text.put("PRINV" + number + order.zfill(3)).write(cls.haru.getX() - 115, 65).flush()

    def setOrderNumber(cls, number):
        cls.setFont("Regular",9.5,[0.25,0.25,0.25])
        cls.text.put(number).write(cls.haru.getX() - 115, 91).flush()

    def setTermLimit(cls, term_limit):
        cls.setFont("Regular", 9,[0.25,0.25,0.25])
        cls.text.put(term_limit).write(25 + 65, 199).flush()

    def setPrice(cls, price):
        super(cls.__class__, cls).setPrice(u'ご請求金額（税込）', price)

    def createObject(cls):
        return cls.haru

if __name__ == '__main__':

    haru	= LibHaru()
    invform	= InvoiceForm(haru)

    for x in dir(invform):
        print x

    haru.close()
