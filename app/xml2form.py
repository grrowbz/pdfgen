#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# libharu test -- haru_demo.py
#

import os, sys
from ctypes import *
from libharu import *
from libxml2form import *

def main():

	haru	= LibHaru()
	xml		= Libxml2form()
	action	= {'rectangle': { 'func':'rect', 'attrib':['width', 'height', 'line', 'fill']} }

	xml.open_xml('../assets/tpl/estimate.xml')
	PAGE_SIZE	= globals()[xml.element('doc', 'page_size')]
	LANDSCAPE	= globals()[xml.element('doc', 'landscape')]

	haru.open().page_setsize(PAGE_SIZE , LANDSCAPE).mbEnable(xml.element('doc', 'language'))

	draw	= HaruDraw(haru)
	for e in xml.itr_elements('draw'):
		_func	= action[e.get("type")]["func"]
		_posx	= e.get("position_x")
		_posy	= e.get("position_y")
		_attr	= action[e.get("type")]["attrib"]
		_rgb	= ('line', 'fill', 'color')

		if 'fill' in e.attrib:
			_func	+= '_with_fill'

		try:
			method	= getattr(draw, _func)
		except AttributeError:
			print "No have method %s in %s", [_func, draw.__class__.__name__]

		#method(_posx, _posy, *[ [1,1,1] if attr in _rgb else e.get(attr) for attr in _attr if attr in e.attrib ])
			

	haru.close()
	return 0

if HPDF_NOPNGLIB:
	printf("WARNING: if you want to run this demo, \n"
			"make libhpdf with HPDF_USE_PNGLIB option.\n")
	sys.exit(1)
else:
    main()
