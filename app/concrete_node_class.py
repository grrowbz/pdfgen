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
            return true if attrib_name in cls.node.attrib else false
        else:
            for attr_n in attrib_name:
                continue if attr_n in cls.node.attrib else break
            else:
                return true
            return false
        pass

    def x(cls):
        return self.node.attrib['position_x'] \
            if 'position_x' in self.node.attrib else false

    def y(cls):
        return self.node.attrib['position_y'] \
            if 'position_y' in self.node.attrib else false

    def width(cls):
        return self.node.attrib['width'] \
            if 'width' in self.node.attrib else false

    def height(cls):
        return self.node.attrib['height'] \
            if 'height' in self.node.attrib else false

    def getPosition(cls):
        return [cls.x, cls.y]

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

