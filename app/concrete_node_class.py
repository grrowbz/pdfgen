#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# concreate node class
#

import os, sys

class CNodeClass():

	def __init__(self, node): 
		self.node	= node
		pass

	def isExists(cls, attrib_name):
		if type(attrib_name) == str:
			for a in cls.node.attrib:
				return True if a == attrib_name else False
		else:
			for a in cls.node.attrib:
				if a in attrib_name:
					print a 
					print attrib_name
					continue
				else: break
			else:
				return True 
			return False 
		pass

	def __getAttrIntValue(cls, attrib_name):
		return int(cls.node.attrib[attrib_name]) \
			if attrib_name in cls.node.attrib else False

	def __getAttrStrValue(cls, attrib_name):
		return str(cls.node.attrib[attrib_name]) \
			if attrib_name in cls.node.attrib else False

	def equalAttrValue(cls, attrib_name, attribute):
		if cls.isExists(attrib_name):
			if cls.__getAttrStrValue(attrib_name) == attribute:
				return True
		return False

	def x(cls):
		return cls.__getAttrIntValue('position_x')

	def y(cls):
		return cls.__getAttrIntValue('position_y')

	def width(cls):
		return cls.__getAttrIntValue('width')

	def height(cls):
		return cls.__getAttrIntValue('height')

	def border(cls):
		return cls.__getAttrIntValue('border')

	def getPosition(cls):
		return [cls.x(), cls.y()]

	"""
	def __init__(cls, haru):
		SuperHaruObject.__init__(cls, haru)
		pass

	def put_image(cls, fname, x, y, width, height):
		__pdf	= cls.pdf()
		image	= HPDF_LoadPngImageFromFile (__pdf, fname)

		HPDF_Page_DrawImage (cls.page(), image, x, y, width, height)
		return cls
	"""

