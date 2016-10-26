#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# libharu test -- haru_demo.py
#

import os, sys
from basic_form import *
from ctypes import *
from libharu import *

class PurchaseOrderForm(BasicForm):

    def __init__(self, haru):

        super(self.__class__, self).__init__(haru)

        ## Header 
        self.text.open_font(self.font["Heavy"]).set_style(16,[1,1,1])
        self.text.put(u'発　注　書').write_with_align("center", 0, 47).flush()

        ## invoice meta information
        self.setFont("Regular",9.5,[0.25,0.25,0.25])
        self.text.put(u'注文No：').write(self.haru.getX() - 160, 65).flush()

        ## greeting message field
        MESSAGE1	= u'下記の通り発注致します。'

        self.text.set_style(10.5,[0.2,0.2,0.2])
        self.text.put(MESSAGE1).write(29, 145).flush()

        ## invoice infomation
        self.setFont("Regular", 9,[0.25,0.25,0.25])
        self.draw.line(25, 203, 290, 1, [0.27, 0.27, 0.27])
        self.draw.line(25, 221, 290, 1, [0.27, 0.27, 0.27])
        self.draw.line(25, 239, 290, 1, [0.27, 0.27, 0.27]) 

        self.text.put(u'納 入 期 限 　 ：').write(25, 199).flush()
        self.text.put(u'納 入 方 式 　 ：').write(25, 217).flush()
        self.text.put(u'支 払 条 件 　 ：').write(25, 235).flush()

    def setClientName(cls, client_name):
        cls.setFont("Regular", 12,[0.25,0.25,0.25])
        cls.text.put(u'御中').write(240, 111).flush()
        cls.setFont("Regular", 14,[0.25,0.25,0.25])
        cls.text.put(u'株式会社Grrow test').write(27, 111).flush()

        cls.setFont("Regular", 12,[0.25,0.25,0.25])
        length  = cls.haru.getX() - (len(client_name) * 13)
        cls.text.put(client_name).write(length, 149).flush()

    ### invoice meta infomation set methods 
    def setProjectNumber(cls, number):
        cls.text.open_font(cls.font["Regular"]).set_style(9.5,[0.25,0.25,0.25])
        cls.text.put("PRORD" + number).write(cls.haru.getX() - 115, 65).flush()

    ## invoice infomation set method
    def setDeliveryDeadline(cls, date):
        cls.setFont("Regular",9,[0.25,0.25,0.25])
        cls.text.put(date).write(25 + 65, 199).flush()

    def setDeliveryMethod(cls, method):
        cls.setFont("Regular",9,[0.25,0.25,0.25])
        cls.text.put(method).write(25 + 65, 216).flush()

    def setPaymentTerms(cls, terms):
        cls.setFont("Regular",9,[0.25,0.25,0.25])
        cls.text.put(terms).write(25 + 65, 234).flush()

    def setPrice(cls, price):
        super(cls.__class__, cls).setPrice(u'発注金額（税込）', price)

    def createObject(cls):
        return cls.haru

if __name__ == '__main__':

	haru	= LibHaru()
	form	= PurchaseOrderForm(haru)

	for x in dir(form):
		print x
	
	haru.close()

