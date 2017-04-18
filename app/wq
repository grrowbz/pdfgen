#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 sts=4 et sta ai fenc=utf-8:
#
#   parser utility class
#

class ParserUtility():

    cursor      = [[0,0]] * 2
    elmHeight   = 0

    def __init__(self): 
        pass

    def setCursor(cls, *args):
        position    = args
        if len(args) < 2: position = args[0]
        cls.cursor[0]   = cls.getCursor()
        cls.cursor[1]   = (position[0], position[1])
        return cls

    def getCursor(cls, pos = None ):
        return cls.cursor[1][0], cls.cursor[1][1]

    def backCursor(cls):
        cls.cursor[1]   = (cls.cursor[0][0], cls.cursor[0][1])
        return cls

    def setElmHeight(cls, height):
        cls.elmHeight   = height
        return cls.elmHeight

    def getElmHeight(cls):
        return cls.elmHeight

    def clearElmHeight(cls):
        elmHeight   = 0
        return cls
