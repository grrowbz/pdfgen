#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#
# concreate node class
#

import os, sys, re

class CNodeClass():

	def __init__(self, node): 
		self.node	= node
		self.attrib	= []
		for attrib in self.node.attrib:
			self.attrib.append(attrib)

	### 属性値の存在確認メソッド。
	### 全ての属性値が含まれていればTrue
	def isExists(cls, attrib_name):
		return cls._exists(attrib_name, 'all')

	### 属性値の存在確認メソッド。
	### 一つでも含まれる属性値があればtrue
	def hasExists(cls, attrib_name):
		return cls._exists(attrib_name, 'has')
		
	def _exists(cls, attrib_name, mode):
		if type(attrib_name) == list:
			if mode == 'all':
				for a in attrib_name:
					## attrib_name内の要素を全てチェック。
					if a not in cls.getAttrib(): return False 
				else:
					return True
			elif mode == 'has':
				for a in attrib_name:
					## attrib_name内の要素を全てチェック。
					if a in cls.getAttrib(): return True
				else:
					return False
		else:
			return attrib_name in cls.getAttrib()
		
	def getAttrib(cls):
		return cls.attrib

	def getChildNodes(cls):
		return list(cls.node)

	def equalAttrValue(cls, attrib_name, attribute):
		if cls.isExists(attrib_name):
			if cls.__getAttrStrValue(attrib_name) == attribute:
				return True
		return False
	
	def text(cls):
		text	= cls.node.text
		retVal	= list()
		strArry = re.split("\\n", text.encode("utf-8"))
		if len(strArry) > 1:
			for st in strArry:
				if len(st.strip()) > 1: retVal.extend([ unicode(st, "utf-8").strip(), "\n"])
		else:
			retVal.append(text.strip())
		return "".join(retVal)

	def x(cls): return cls.__getAttrIntValue('position_x')
	def y(cls): return cls.__getAttrIntValue('position_y')
	def width(cls): return cls.__getAttrIntValue('width')
	def height(cls): return cls.__getAttrIntValue('height')
	def getPosition(cls): return [cls.x(), cls.y()]
	def size(cls): return cls.__getExtraAttrValue("int", 'size')

	def color(cls):
		color_code	= cls.__getExtraAttrValue("str", 'color')
		if not color_code: return False
		return cls._color(color_code)

	def borderColor(cls):
		color_code	= cls.__getExtraAttrValue("str", 'border_color')
		if not color_code: return False
		return cls._color(color_code)

	def _color(cls, color_code):
		### カラーコードを2桁毎に分割し10進数に変換した後、255で割る
		### 例: 33 → 51 / 255 → 0.2
		color	= map(lambda n: round(float(int(str(n), 16)) / 255, 2), 
				 [color_code[(idx-1):idx+1] for idx in range(len(color_code)) if idx % 2 ])
		return color

	def name(cls): return cls.__getExtraAttrValue("str", 'name')
	def type(cls): return cls.__getExtraAttrValue("str", 'type')

	def border(cls): return cls.__getExtraAttrValue("int", 'border')
	def borderStyle(cls): return cls.__getExtraAttrValue("str", 'border_style')
	def borderBottom(cls): return cls.__getExtraAttrValue("int", 'border_bottom')
	def borderTop(cls): return cls.__getExtraAttrValue("int", 'border_top')

	def summary(cls): return cls.__getExtraAttrValue("str", 'summary')
	def font(cls): return cls.__getExtraAttrValue("str", 'font')
	def fontSize(cls): return cls.__getExtraAttrValue("int", 'font_size')
	def textAlign(cls): return cls.__getExtraAttrValue("str", 'align')
	def paddingBottom(cls): return cls.__getExtraAttrValue("int", 'padding_bottom')
	def paddingTop(cls): return cls.__getExtraAttrValue("int", 'padding_top')
	def paddingRight(cls): return cls.__getExtraAttrValue("int", 'padding_right')
	def paddingLeft(cls): return cls.__getExtraAttrValue("int", 'padding_left')

	### XMLタグ内のプロパティ値（文字列）の取得メソッド
	### name		__getAttrStrValue
	### return		unicode string
	def __getAttrStrValue(cls, attrib_name):
		return unicode(cls.node.attrib[attrib_name]) \
			if attrib_name in cls.node.attrib else False

	def __getAttrIntValue(cls, attrib_name):
		if type(attrib_name) == int:
			return int(cls.node.attrib[attrib_name]) \
				if attrib_name in cls.node.attrib else False
		else:
			return round(float(cls.node.attrib[attrib_name]), 2) \
				if attrib_name in cls.node.attrib else False

	### XMLタグ内の拡張プロパティ値の取得メソッド
	### プロパティが定義されていない場合はFlaseを返す
	def __getExtraAttrValue(cls, type, attrib_name):
		if cls.isExists(attrib_name):
			if type == "str":
				return cls.__getAttrStrValue(attrib_name)
			elif type == "int":
				return cls.__getAttrIntValue(attrib_name)
		else:
			return False

