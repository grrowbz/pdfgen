#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 fenc=utf-8:
#

import os, sys
import libharu
import invoice_form, estimate_form, purchase_order_form
import json

def lambda_handler(event, context):

	## 必須な値のチェックと足りない場合にエラー
	## を返す処理 2016/10/31 未実装
	## context['template'] は必須

	haru        = libharu.LibHaru()
	module_name = context['template'] + "_form"
	class_name  = ''.join(map(lambda n:n[0].upper() + n[1:], module_name.split("_")))

	### 対象になるモジュール（請求書や見積書）の呼び出し処理。
	### 最終的にはモジュールを適宜変える形ではなく、XMLテンプレートの名称を外から与える
	### 形式に変更する。
	## 無効なモジュール名の呼び出しを検出して、エラーを
	## 返す処理を前段で入れる 2016/10/31 未実装
	form        = getattr(sys.modules[module_name], class_name)(haru)

	'''
	メソッドの自動呼び出しを実装中。とりあえず一旦中止
	for attr in filter(lambda x: x != 'template',context.keys()):
		method  = 'set'+''.join(map(lambda n:n[0].upper() + n[1:], attr.split("_")))
		if hasattr(form, method):
		    getattr(form, method)(context[attr])
		    print method
	''' 
	setter		= form.getValueSetter()

	for name in context['data'].keys():
		if name in setter.getPlaceHolderKeys():
			form.renderPlaceHolder(setter.getPlaceHolder(name), context['data'][name])

	if context['template'] == "invoice":
		form.setOrderNumber(context['data']['order_no'])

	form.setDeliverables(context['data']['deliverables'])
	form.setRemarksColumn(context['data']['remarks_column'])

	subtotal = 0
	"""
	if context['data']['item_data'] :
		p = json.loads(context['data']['item_data'])
	for x in range(1,21):
		if( p.has_key(unicode(x)) ):
			if (p[unicode(x)].has_key(u'qty')):
				subtotal += int(p[unicode(x)][u'price'])
				form.setItemData(   x, x,
						p[unicode(x)][u'item'],
						p[unicode(x)][u'qty'],
						p[unicode(x)][u'unit'],
						p[unicode(x)][u'uprice'],
						p[unicode(x)][u'price'])
			else:
				form.setItemDataForOnlySubTitle(   x, x, p[unicode(x)][u'item'])
	"""
		## form.setPrice(subtotal)

	form.createObject().save('/tmp/.tmp.pdf')
	with open('/tmp/.tmp.pdf', 'r') as f:
		return f.read()
	## ここはちゃんと動作する？要確認
	haru.close()
	f.close()
