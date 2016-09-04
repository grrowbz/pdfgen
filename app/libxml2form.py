#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# libxml2form -- libxml2form.py
#

import os, sys
from ctypes import *
from xml.etree.ElementTree import *

class Libxml2form():

	def __init__(self):
		self.__xmltree		= None
		self.__toptree		= None
		pass

	def open_xml(self, fname):
		self.__xmltree	= ElementTree()
		if (not self.__xmltree):
			printf ("error: cannot open target file: %s \n", fname)
			return 1

		self.__xmltree.parse(fname)
		self.__toptree		= self.__xmltree.getroot()
		return self

	def element(self, elmName, attr):
		__tag	= self.find(elmName)
		if ('None' == __tag.tag):
			return false
		return __tag.get(attr)

	def itr_elements(self, elmName):
		itr	= LibxmlIteration(self.findall(format(elmName)))
		return itr;

	def find(self, elmName):
		return self.__toptree.find(elmName)

	def findall(self, elmName):
		return self.__toptree.findall(".//{}".format(elmName))
		
		

class LibxmlIteration():

	def __init__(self, *etrList):
		self.__etrList	= etrList[0]
		self.__length	= 0
		pass
	def __iter__(self): return self
	def next(self):
		if self.__length == len(self.__etrList):
			raise StopIteration()
		value = self.__etrList[self.__length]
		self.__length += 1
		return value

