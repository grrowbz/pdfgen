#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#

import os, sys
from collections import namedtuple
from ctypes import *
from libharu import *
from concrete_node_class import CNodeClass
from value_setter_class import ValueSetterClass
from parser_utility import ParserUtility

class BasicForm(object):

	haru		= ""
	text		= ""
	draw		= ""
	font		= {}
	setter		= ""
	util		= ""
	cursor		= [[0, 0]] * 2

	def __init__(self, haru):

		self.haru	= haru
		self.draw	= HaruDraw(self.haru)
		self.text	= HaruText(self.haru)
		self.setter	= ValueSetterClass(self)	
		self.util	= ParserUtility()
		self.render("../assets/tpl/basic.xml")

	def __getPosAttr(cls, node):
		return [int(node.attrib['position_x']), int(node.attrib['position_y'])]

	def getValueSetter(cls):
		return cls.setter

	def renderPlaceHolder(cls, ph, ctx):
		cls.text.open_font(ph['font']).set_style(ph['size'],ph['color'])
		cls.text.put(ctx).write(ph['x'], ph['y']).flush()

	##################################
	#### renderメソッド系
	#################################

	def parseHeader(cls, node):
		for e in list(node):
			nd	= CNodeClass(e)
			if e.tag == "font":
				cls.font[e.attrib['name']] = {	"src"  : e.attrib['src'],
												"size" : nd.size() if nd.isExists("size") else False,
												"color": nd.color() if nd.isExists("color") else False }

	### XMLパーサー。__renderのラッパー。初めのharuによるPDFインスタンスの生成を含むparse処理
	def render(cls, xml):
		import xml.etree.ElementTree as parser
		root	= parser.parse(xml).getroot()
		doc		= root.find("doc")
		cls.haru.open().page_setsize(eval(doc.attrib['page_size']),
									 eval(doc.attrib['landscape'])).mbEnable(doc.attrib['language'])
		cls.__render(xml)

	### XMLパーサー。__renderのラッパー。既に開かれたPDFインスタンスへの上書き処理
	def overwriteRender(cls, xml):
		cls.__render(xml)

	### XMLパーサー。XMLの解析と描画メソッドのコール
	def __render(cls, xml):
		import xml.etree.ElementTree as parser

		### 最上位要素の処理。
		root	= parser.parse(xml).getroot()
		for idx,n in enumerate(root):
			if n.tag == "head": cls.parseHeader(n)
			elif n.tag == "doc": docIdx = idx

		### ドキュメント要素内を処理
		for e in list(root[docIdx]):
			nd	= CNodeClass(e)
			msgLog = "[PARSE INFO] [<" + e.tag + ">]"
			if nd.isExists("summary"):
				msgLog +=" (summary=" + nd.summary() + ")"

			if e.tag == "block": pass
			elif e.tag == "textarea": cls.renderTextArea(e)
			elif e.tag == "table": cls.renderTable(e)

			### hrはメソッドコールでなくダイレクトに処理
			elif e.tag == "hr": 
				xPos, yPos	  = cls.__getPosAttr(e)
				cls.draw.line(xPos, yPos, int(e.attrib['width']), 1, [0.27, 0.27, 0.27])
				if nd.equalAttrValue("border_style", "double"):
					cls.draw.line(xPos, yPos+2, int(e.attrib['width']), 1, [0.27, 0.27, 0.27])
			else:
				msgLog += " this tag have no parser. Just pass to ignore." 

			### デバッグメッセージの表示
			print msgLog

	#### 属性値:border、border_style、border_colorの処理
	def __attribBorder(cls, nd):
		x, y	= cls.util.getCursor()

		### Borderのカラー設定
		_color	= nd.borderColor() if nd.isExists('border_color') else [0, 0, 0]
		_style	= nd.borderStyle() if nd.isExists('border_style') else False

		if nd.hasExists(['border_top', 'border_bottom', 'border']):
			for attr in nd.getAttrib():
				### border_topの場合、yPosから高さ分引く必要がある。
				if attr in ['border_top', 'border']: 
					cls.draw.line(x, y, nd.width(), nd.borderTop(), _color)

				if attr in ['border_bottom', 'border']: 
					cls.draw.line(x, y + nd.height(), nd.width(), nd.borderBottom(), _color)
					if _style == "double":
						cls.draw.line(x, y + nd.height() + 2, nd.width(), nd.borderTop(), _color)

				if attr in ['border_left', 'border']: 
					cls.draw.vline(x, y + nd.height(), nd.height(), 1, _color)

				if attr in ['border_right', 'border']: 
					cls.draw.vline(x + nd.width(), y + nd.height(), nd.height(), 1, _color)

	def __attribPadding(cls, nd, type="None"):
		x, y	= cls.util.getCursor()

		if nd.hasExists(['padding_top', 'padding_bottom']):
			for attr in nd.getAttrib():
				if attr == 'padding_top': cls.util.setCursor(x, y + nd.paddingTop())
				elif attr == 'padding_bottom': cls.util.setCursor(x, y - nd.paddingBottom())

		if type == "Before": 
			if nd.hasExists('padding_left'):
				for attr in nd.getAttrib():
					if attr == 'padding_left': cls.util.setCursor(x + nd.paddingLeft(), y)
		elif type == "After":
			if nd.hasExists('padding_right'):
				for attr in nd.getAttrib():
					if attr == 'padding_right': cls.util.setCursor(x + nd.paddingRight(), y)
			
		
	def __childNodeParser(cls, nd, font, font_size,font_color):
		setter	= cls.setter
 		x, y	= cls.util.getCursor()
		cls.util.setCursor(x, y +cls.text.getFontHeight())
		
		for e in nd.getChildNodes():
			cN		= CNodeClass(e)
			cls.__attribPadding(cN, 'Before')
			x, y	= cls.util.getCursor()

			if e.tag == "text":
				if cN.isExists('align'):
					cls.util.setCursor(x + nd.width(), y)
					cls.text.put(cN.text()).write_with_align(cN.textAlign(), nd.width(), x, y)
				else:
					cls.util.setCursor(x + cls.text.put_with_width(cN.text()), y)
					cls.text.write(x, y)
				cls.text.flush()
			elif e.tag == 'placeholder':
				setter.setPlaceHolder(cN.name(), x, y, nd.width(), cN.type(), font, font_size, font_color)
			elif e.tag == 'br':
				x, y = cls.util.backCursor().getCursor()
				cls.util.setCursor(x, y + cls.text.getFontHeight())
			cls.__attribPadding(cN, 'After')
		else:
			cls.text.flush()

	### 文字列（テキスト領域）描画メソッド
	def renderTextArea(cls, node):
		nd			= CNodeClass(node)
		xPos, yPos	= cls.util.setCursor(nd.getPosition()).getCursor()

		cls.__attribBorder(nd)		 ### attribute border process
		cls.__attribPadding(nd)		 ### attribute padding process

		if nd.isExists('auto_reduced'):
			pass

		font			= cls.font[nd.font()]["src"]
		font_size		= nd.fontSize() if nd.isExists('font_size') else cls.font[nd.font()]["size"]
		font_color		= nd.fontColor() if nd.isExists('font_color') else cls.font[nd.font()]["color"]

		cls.text.open_font(font).set_style(font_size,font_color)
		cls.__childNodeParser(nd, font, font_size, font_color)

	### 線表描画メソッド
	def renderTable(cls, node):
		nd			= CNodeClass(node)
		tPos, yPos	= nd.getPosition()
		linePos		= yPos

		if not nd.isExists(['position_x', 'position_y', 'width', 'height', 'border']):
			print "not"
		cls.draw.rect(	tPos, yPos, nd.width(), nd.height(), nd.border(), [0.27, 0.27, 0.27])

		## 列(tr)の処理
		for e in list(node):
			if e.tag == "tr":
				cls.setFont("Regular",9,[0.25,0.25,0.25])
				cHeight = int(e.attrib['height'])

				for rl in range(0, int(e.attrib['for'] if 'for' in e.attrib else 1)):
					vertPos = tPos
					### td/th の処理
					for cell in list(e):
						cWidth = int(cell.attrib["width"])
						## --- ヘッダーが(th)の場合の処理
						if cell.tag == "th":
							### ヘッダーのテキストを描画
							cls.text.put(unicode(cell.text)).\
								write_with_align('center', cWidth,\
								vertPos, yPos + cHeight - 2).flush()

							cls.draw.rect(	vertPos, linePos, cWidth, cHeight,\
								1, [0.27, 0.27, 0.27])
						## --- ヘッダーthの処理：ここまで

						## --- ヘッダーtdの処理
						elif cell.tag == "td":
							cls.draw.vline(vertPos, linePos+cHeight, cHeight, 1, [0.27, 0.27, 0.27])
							cls.draw.dash_line(vertPos, linePos, cWidth, 0.7, [2, 1], [0.3, 0.3, 0.3])

						## --- ヘッダーtdの処理：ここまで
						vertPos += cWidth
					else:
						### tdの最終セルの最後尾の縦線描画
						cls.draw.vline(vertPos, linePos+cHeight, cHeight, 1, [0.27, 0.27, 0.27])
						linePos += cHeight
					### td/thの処理：ここまで
		## 列(tr)の処理：ここまで

	def setFont(cls, name, weight, color):
		cls.text.open_font(cls.font[name]["src"]).set_style(weight,color)

	def setPrice(cls, title, price):
		subtotal	= int(price)
		tax			= int(subtotal * 0.08)
		price		= subtotal + tax

		cls.setFont("Regular",10,[0.25,0.25,0.25])
		textObj = cls.text.put(u"￥" + "{:,}".format(subtotal))
		textObj.write_with_align('right', 85, 480, 646, 3 ).flush()

		textObj = cls.text.put(u"￥" + "{:,}".format(tax))
		textObj.write_with_align('right', 85, 480, 668, 3 ).flush()

		textObj = cls.text.put(u"￥" + "{:,}".format(price))
		textObj.write_with_align('right', 85, 480, 692, 3 ).flush()

		cls.setFont("Regular",13,[0.25,0.25,0.25])
		cls.text.put(title).write(25, 276).flush()

		cls.setFont("Regular",15,[0.25,0.25,0.25])
		textObj = cls.text.put(u"￥" + "{:,}".format(int(price)))
		textObj.write_with_align('right', 166, 150, 276, 3 ).flush()

	def createObject(cls):
		return cls.haru

