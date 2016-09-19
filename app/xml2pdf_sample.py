#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#

import os, sys
import libxml2form

def main():

	xml		= libxml2form.Libxml2form()
	action	= {'rectangle': { 'func':'rect', 'attrib':['width', 'height', 'line', 'fill']} }

	xml.open_xml(os.path.join(os.path.dirname(__file__), '../assets/tpl/invoice.xml'))
	## PAGE_SIZE	= globals()[xml.element('doc', 'page_size')]
	## LANDSCAPE	= globals()[xml.element('doc', 'landscape')]

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

			
	return 0

if __name__ == '__main__':
    main()
