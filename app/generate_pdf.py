#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
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

    ## 無効なモジュール名の呼び出しを検出して、エラーを
    ## 返す処理を前段で入れる 2016/10/31 未実装
    form        = getattr(sys.modules[module_name], class_name)(haru)

    for attr in filter(lambda x: x != 'template',context.keys()):
        method  = 'set'+''.join(map(lambda n:n[0].upper() + n[1:], attr.split("_")))
        if hasattr(form, method):
            getattr(form, method)(context[attr])
            print method

    if context['template'] == "invoice":
        form.setProjectNumber(context['project_no'], context['order_no'])
        form.setOrderNumber(context['order_no'])
    else:
        form.setProjectNumber(context['project_no'])

    if context['template'] in ["estimate", "purchase_order"]:
        form.setDeliveryDeadline(context['delivery_deadline'])
        form.setDeliveryMethod(context['delivery_method'])
        form.setPaymentTerms(context['payment_terms'])
    elif context['template'] == "invoice":
        form.setTermLimit(context['term_limit'])
 
    form.setCreateDate(context['create_date'])
    form.setClientName(context['client_name'])
    form.setTitle(context['title'])
    form.setPrice(context['price'])

    form.setDeliverables(context['deliverables'])
    form.setRemarksColumn(context['remarks_column'])

    if context['item_data'] :
        p = json.loads(context['item_data'])
        for x in range(1,21):
            if( p.has_key(unicode(x)) ):
                if (p[unicode(x)].has_key(u'num')):
                    form.setItemData(   x, x,
                                        p[unicode(x)][u'item'],
                                        p[unicode(x)][u'num'],
                                        p[unicode(x)][u'unit'],
                                        p[unicode(x)][u'uprice'],
                                        p[unicode(x)][u'price'])
                else:
                    form.setItemDataForOnlySubTitle(   x, x, p[unicode(x)][u'item'])
    
    form.createObject().save('/tmp/.tmp.pdf')
    with open('/tmp/.tmp.pdf', 'r') as f:
        return f.read()
    ## ここはちゃんと動作する？要確認
    haru.close()
    f.close()
