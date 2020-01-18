#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import os, sys
sys.path.append('./')
import libharu
import invoice_form, estimate_form, purchase_order_form
import json

def lambda_handler(event, context):

    ## 必須な値のチェックと足りない場合にエラー
    ## を返す処理 2016/10/31 未実装
    ## event['template'] は必須

    haru        = libharu.LibHaru()
    params      = json.loads(event['body'])

    module_name = params['template'] + "_form"
    class_name  = ''.join(map(lambda n:n[0].upper() + n[1:], module_name.split("_")))

    ## 無効なモジュール名の呼び出しを検出して、エラーを
    ## 返す処理を前段で入れる 2016/10/31 未実装
    form        = getattr(sys.modules['app.' + module_name], "InvoiceForm")(haru)

    '''
    メソッドの自動呼び出しを実装中。とりあえず一旦中止
    for attr in filter(lambda x: x != 'template',params.keys()):
        method  = 'set'+''.join(map(lambda n:n[0].upper() + n[1:], attr.split("_")))
        if hasattr(form, method):
            getattr(form, method)(params[attr])
            print method
    '''

    return {
        'isBase64Encoded': False,
        'statusCode': 200,
        'headers': {},
        'body': '{"message": "Hello from AWS Lambda"}'
    }


    if params['template'] == "invoice":
        form.setProjectNumber(params['project_no'], params['order_no'])
        form.setOrderNumber(params['order_no'])
    else:
        form.setProjectNumber(params['project_no'])

    if params['template'] in ["estimate", "purchase_order"]:
        form.setDeliveryDeadline(params['delivery_deadline'])
        form.setDeliveryMethod(params['delivery_method'])
        form.setPaymentTerms(params['payment_terms'])
    elif params['template'] == "invoice":
        form.setTermLimit(params['term_limit'])
 
    form.setCreateDate(params['create_date'])
    form.setClientName(params['client_name'])
    form.setTitle(params['title'])

    form.setDeliverables(params['deliverables'])
    form.setRemarksColumn(params['remarks_column'])

    subtotal = 0
    if params['item_data'] :
        p = json.loads(params['item_data'])
        for x in range(1,22):
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
    form.setPrice(subtotal)

    form.createObject().save('/tmp/.tmp.pdf')
    with open('/tmp/.tmp.pdf', 'r') as f:
        return f.read()
    ## ここはちゃんと動作する？要確認
    haru.close()
    f.close()
