#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#

import os, sys
from ctypes import *
from libharu import *

class ValueSetterClass(object):

	parser		= ""
	text		= ""
	draw		= ""
	font		= ""

	def __init__(self, parser):

		self.parser	= parser


