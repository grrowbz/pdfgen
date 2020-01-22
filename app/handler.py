#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import os, sys, ctypes
from app import libharu
from app import invoice_form
## import app.estimate_form as estimate_form
## import app.purchase_order_form as purchase_order_form
import json, base64, logging
import boto3

ctypes.cdll.LoadLibrary(os.path.join('lib/', 'libpng15.so.15'))
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):

    ## 必須な値のチェックと足りない場合にエラー
    ## を返す処理 2016/10/31 未実装
    ## event['template'] は必須

    haru        = libharu.LibHaru()
    _params     = event['body'] if event.get('body') else event
    params      = _params

    module_name = params['template'] + "_form"
    class_name  = ''.join(map(lambda n:n[0].upper() + n[1:], module_name.split("_")))

    logger.info("テンプレートモジュールの読込開始")

    ## 無効なモジュール名の呼び出しを検出して、エラーを
    ## 返す処理を前段で入れる 2016/10/31 未実装
    form        = getattr(sys.modules['app.' + module_name], "InvoiceForm")(haru)

    logger.info("テンプレートモジュールの読込完了")
    logger.info(module_name)

    '''
    メソッドの自動呼び出しを実装中。とりあえず一旦中止
    for attr in filter(lambda x: x != 'template',params.keys()):
        method  = 'set'+''.join(map(lambda n:n[0].upper() + n[1:], attr.split("_")))
        if hasattr(form, method):
            getattr(form, method)(params[attr])
            print method
    '''

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
    form.createObject().save('/tmp/example.pdf')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket('grrow.space')

    with open('/tmp/example.pdf', 'r') as f:

        bucket.put_object(
            Body = f.read(),
            Key = "hogehoge.pdf",
            ContentType='application/pdf'
        )

        return {
            "Content-Type": "application/pdf",
            "Location": "https://s3-ap-northeast-1.amazonaws.com/grrow.space/hogehoge.pdf"
        }
    ## ここはちゃんと動作する？要確認
    haru.close()
    f.close()
