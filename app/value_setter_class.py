#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#

import os, sys
from ctypes import *
from libharu import *

class ValueSetterClass(object):

	parser		= ""
	pHolder		= {} 
	draw		= ""
	font		= ""

	def __init__(self, parser):

		self.parser	= parser

	def setPlaceHolder(cls,name, x, y, width, type, font, size, font_color):
		cls.pHolder[name]	= { "x": x, "y": y, "width": width, "type": type, "font": font, "size": size, "color": font_color }

	def getPlaceHolderKeys(cls):
		return cls.pHolder.keys()

	def getPlaceHolder(cls, name):
		return cls.pHolder[name]
