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

class EstimateForm(BasicForm):

	def __init__(self, haru):

		super(self.__class__, self).__init__(haru)
		self.overwriteRender("../assets/tpl/estimate.xml")

		## Header 
		self.text.open_font(self.font["Heavy"]["src"]).set_style(16,[1,1,1])
		self.text.put(u'御　見　積　書').write_with_align("center", self.haru.getX(), 0, 47).flush()

		"""
		## invoice meta information
		self.setFont("Regular",9.5,[0.25,0.25,0.25])
		self.text.put(u'見積No：').write(self.haru.getX() - 160, 65).flush()

		## greeting message field
		MESSAGE1	= u'下記の通りお見積り致しますので、'
		MESSAGE2	= u'よろしくお願い申し上げます。'

		self.text.set_style(10.5,[0.2,0.2,0.2])
		self.text.put(MESSAGE1).write(29, 145).flush()
		self.text.put(MESSAGE2).write(29, 158).flush()

		## invoice infomation
		self.setFont("Regular", 9,[0.25,0.25,0.25])
		self.draw.line(25, 203, 290, 1, [0.27, 0.27, 0.27])
		self.draw.line(25, 221, 290, 1, [0.27, 0.27, 0.27])
		self.draw.line(25, 239, 290, 1, [0.27, 0.27, 0.27])
 
		self.text.put(u'納 入 期 限 　 ：').write(25, 199).flush()
		self.text.put(u'納 入 方 式 　 ：').write(25, 217).flush()
		self.text.put(u'御 支 払 条 件 ：').write(25, 235).flush()

		self.setCompanyInfo()
		self.setSignBox()
		"""

	### invoice meta infomation set methods 
	def setProjectNumber(cls, number):
		cls.text.open_font(cls.font["Regular"]["src"]).set_style(9.5,[0.25,0.25,0.25])
		cls.text.put("PR" + number).write(cls.haru.getX() - 115, 65).flush()

	## invoice infomation set method
	def setDeliveryDeadline(cls, date):
		return True
		cls.setFont("Regular",9,[0.25,0.25,0.25])
		cls.text.put(date).write(25 + 65, 199).flush()

	def setDeliveryMethod(cls, method):
		return True
		cls.setFont("Regular",9,[0.25,0.25,0.25])
		cls.text.put(method).write(25 + 65, 216).flush()

	def setPaymentTerms(cls, terms):
		return True
		cls.setFont("Regular",9,[0.25,0.25,0.25])
		cls.text.put(terms).write(25 + 65, 234).flush()

	def setPrice(cls, price):
		return True
		##super(cls.__class__, cls).setPrice(u'お見積金額（税込）', price)

	def createObject(cls):
		return cls.haru

if __name__ == '__main__':

    haru	= LibHaru()
    form	= EstimateForm(haru)

    for x in dir(form):
        print x

    haru.close()
