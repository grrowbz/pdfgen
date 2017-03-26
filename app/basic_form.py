#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 fenc=utf-8:
#

import os, sys
from ctypes import *
from libharu import *
from concrete_node_class import CNodeClass
from value_setter_class import ValueSetterClass

class BasicForm(object):

	haru		= ""
	text		= ""
	draw		= ""
	font		= {}
	setter		= ""
	textdata	= {}

	def __init__(self, haru):

		self.haru	= haru
		self.draw	= HaruDraw(self.haru)
		self.text	= HaruText(self.haru)
		self.setter	= ValueSetterClass(self)	
		self.render("../assets/tpl/basic.xml")

		"""
		## Header 
		self.draw.rect_with_fill(25, 27, 545, 25, [0.28, 0.28, 0.28])

		InfoBoxY  = 630
		BottomBoxHeight = 70
		### 納品物
		self.setFont("Regular",10,[0.25,0.25,0.25])
		self.text.put(u'納品物').write(32, InfoBoxY + 38).flush()
		self.draw.rect(25, InfoBoxY, 45, BottomBoxHeight - 2, 1, [0.27, 0.27, 0.27])
		self.draw.rect(70, InfoBoxY, 235, BottomBoxHeight - 2, 1, [0.27, 0.27, 0.27])

		### Price Box
		self.setFont("Regular",11,[0.25,0.25,0.25])
		self.text.put(u'小計').write(480 - 26, InfoBoxY + 16).flush()
		self.text.put(u'消費税').write(480 - 39, InfoBoxY + 38).flush()
		self.setFont("Regular",12,[0.25,0.25,0.25])
		self.text.put(u'合計').write(480 - 26, InfoBoxY + 62).flush()

		self.draw.rect(480, InfoBoxY, 85, BottomBoxHeight - 2, 1, [0.27, 0.27, 0.27])
		self.draw.line(305, InfoBoxY, 175, 1, [0.27, 0.27, 0.27])
		self.draw.line(305, InfoBoxY + 22, 260, 1, [0.27, 0.27, 0.27])
		self.draw.line(305, InfoBoxY + 46, 260, 1, [0.27, 0.27, 0.27])
		self.draw.line(305, InfoBoxY + 68, 175, 1, [0.27, 0.27, 0.27])

		ItemBoxY = BoxY + 12
		for var in range(1, 21):
			self.draw.dash_line(25, ItemBoxY + 15 * var, 540, 0.7, [2, 1], [0.3, 0.3, 0.3])
		"""

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
				msgLog += " (summary=" + nd.summary() + ")"

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
	def __attribBorder(cls, _nd, x, y):

		### Borderのカラー設定
		_color	= _nd.borderColor() if _nd.isExists('border_color') else [0, 0, 0]
		_style	= _nd.borderStyle() if _nd.isExists('border_style') else False

		if _nd.hasExists(['border_top', 'border_bottom']):
			for attr in _nd.getAttrib():
				### border_topの場合、yPosから高さ分引く必要がある。
				if attr == 'border_top': 
					cls.draw.line(x, y, _nd.width(), _nd.borderTop(), _color)
				elif attr == 'border_bottom': 
					cls.draw.line(x, y, _nd.width(), _nd.borderBottom(), _color)
					if _style == "double":
						cls.draw.line(x, y+2, _nd.width(), _nd.borderTop(), _color)

	def __childNodeParser(cls, _nd, x, y, font, font_size,font_color):
		setter		= cls.setter

		for e in _nd.getChildNodes():
			if e.tag == "text":
				cN	= CNodeClass(e)
				if cN.isExists('text_align'):
					cls.text.put(cN.text()).write_with_align(cN.textAlign(), _nd.width(), x, y).flush()
				else:
					cls.text.put(cN.text()).write(x, y).flush()
				x += cls.text.put_with_width(cN.text())
				cls.text.flush()
			elif e.tag == 'placeholder':
				cN	= CNodeClass(e)
				setter.setPlaceHolder(cN.name(), x, y, _nd.width(), cN.type(), font, font_size, font_color)

	### 文字列（テキスト領域）描画メソッド
	def renderTextArea(cls, node):
		nd			= CNodeClass(node)
		xPos, yPos	= nd.getPosition()

		### attribute border process
		cls.__attribBorder(nd, xPos, yPos)

		if nd.hasExists(['padding_top', 'padding_bottom']):
			for attr in node.attrib:
				if attr == 'padding_top': yPos += nd.paddingTop()
				elif attr == 'padding_bottom': yPos -= nd.paddingBottom()

		if nd.isExists('auto_reduced'):
			pass

		font			= cls.font[nd.font()]["src"]
		font_size		= nd.fontSize() if nd.isExists('font_size') else cls.font[nd.font()]["size"]
		font_color		= nd.fontColor() if nd.isExists('font_color') else cls.font[nd.font()]["color"]

		cls.text.open_font(font).set_style(font_size,font_color)
		cls.__childNodeParser(nd, xPos, yPos, font, font_size, font_color)

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

	def setCompanyInfo(cls):
		## company information
		KABU			= u'株式会社'
		COMPANY_NAME	= u'Grrow'
		POST_NO			= u'〒140-001'
		ADRESS_1		= u'東京都品川区北品川'
		ADRESS_2		= u'1-9-7 トップルーム品川1015'
		PHONE_NO		= u'TEL：090-2420-2989'

		cls.text.open_font(cls.font["Bold"]["src"]).set_style(16,[0.25,0.25,0.25])
		cls.text.put(KABU).write(cls.haru.getX() - 192, 149).flush()
		cls.text.open_font(cls.font["Bold"]["src"]).set_style(19,[0.25,0.25,0.25])
		cls.text.put(COMPANY_NAME).write(cls.haru.getX() - 126, 149).flush()

		cls.text.open_font(cls.font["Regular"]["src"]).set_style(11,[0.25,0.25,0.25])
		cls.text.put(ADRESS_1).write(cls.haru.getX() - 132, 166).flush()
		cls.text.put(ADRESS_2).write(cls.haru.getX() - 166, 179).flush()

		cls.setFont("Regular", 9.5,[0.25,0.25,0.25])
		## 郵便番号の出力位置表示 画面サイズX幅 - 132 - 45
		cls.text.put(POST_NO).write_with_align("right", 45, cls.haru.getX() - 177, 166, 3).flush()
		## 電話番号の設定
		cls.text.put(PHONE_NO).write_with_align("right", 133, cls.haru.getX() - 166, 192).flush()

	def setSignBox(cls):
		### Sign Box
		cls.setFont("Regular",9,[0.25,0.25,0.25])
		cls.text.put(u'承認').write(433, 225).flush()
		cls.text.put(u'担当者').write(508, 225).flush()
		cls.draw.line(400, 230, 160, 1, [0.27, 0.27, 0.27])
		cls.draw.rect(400, 214, 80, 76, 1, [0.27, 0.27, 0.27])
		cls.draw.rect(480, 214, 80, 76, 1, [0.27, 0.27, 0.27])

	def setCreateDate(cls, date):
		cls.setFont("Regular",9.5,[0.25,0.25,0.25])
		cls.text.put(date).write(cls.haru.getX() - 115, 78).flush()

	### client name set method
	def setClientName(cls, client_name):
		return True
		cls.setFont("Regular", 12,[0.25,0.25,0.25])
		cls.text.put(u'様').write(248, 111).flush()
		cls.text.put(client_name).setAutoReduce(215).write(27, 111).flush()

	## project name set method
	def setTitle(cls, title):
		cls.setFont("Regular", 9,[0.25,0.25,0.25])
		cls.text.put(title).write(25 + 65, 182).flush()

	## Font Setting method 
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

	def setDeliverables(cls, deliverables, num=1):
		cls.setFont("Regular",8.5,[0.25,0.25,0.25])
		cls.text.put(deliverables).write(75, 633 + (12 * num)).flush()

	def setRemarksColumn(cls, remarks, num=1):
		cls.setFont("Regular",8.5,[0.25,0.25,0.25])
		cls.text.put(remarks).write(30, 718 + (12 * num)).flush()

	def __align(cls, string, x, width, position):
		print len(string)
		#return (x + width) - len(string)

	def setItemData(cls, LineNo, no, item, qty, unit, uprice, price):
		cls.setFont("Regular",8.5,[0.25,0.25,0.25])
		YPos = 314 + (15 * LineNo) - 3

		cls.text.put(str(no)).write_with_align('center', 25, 25, YPos).flush()
		cls.text.put(unicode(item)).write(50 + 3, YPos).flush()
		cls.text.put(str(qty)).write_with_align('center', 50, 330, YPos).flush()
		cls.text.put(unicode(unit)).write_with_align('center', 35, 380, YPos).flush()

		if (int(uprice) < 0) :
			cls.setFont("Regular",8.5,[1,0,0])
		textObj = cls.text.put(u"￥" + "{:,}".format(int(uprice)))
		textObj.write_with_align('right', 65, 415, YPos, 3 ).flush()
		cls.setFont("Regular",8.5,[0.25,0.25,0.25])

		if (int(uprice) < 0) :
			cls.setFont("Regular",8.5,[1,0,0])
		textObj = cls.text.put(u"￥" + "{:,}".format(int(price)))
		textObj.write_with_align('right', 85, 480, YPos, 3).flush()
		cls.setFont("Regular",8.5,[0.25,0.25,0.25])

	def setItemDataForOnlySubTitle(cls, LineNo, no, item):
		cls.setFont("Regular",8.5,[0.25,0.25,0.25])
		ListPosition = 314 + (15 * LineNo) - 3
		cls.text.put(unicode(no)).write(25 + 10, ListPosition).flush()
		cls.text.put(unicode(item)).write(50 + 3, ListPosition).flush()

	def createObject(cls):
		return cls.haru

