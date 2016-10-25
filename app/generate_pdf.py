#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import os, sys
import libharu
import invoice_form, estimate_form, purchase_order_form

def lambda_handler(event, context):
    haru        = libharu.LibHaru()

    form_list   = { "invoice" : { "mod":"invoice_form", "class":"InvoiceForm" },
                    "estimate" : { "mod":"estimate_form", "class":"EstimateForm" },
                    "purchase_order" : { "mod":"purchase_order_form", "class":"PurchaseOrderForm" }} 

    useform     = form_list[context['template']]
    form        = getattr(sys.modules[useform['mod']], useform['class'])(haru)

    if context['template'] == "invoice":
        form.setProjectNumber(context['project_no'], context['order_no'])
        form.setOrderNumber(context['order_no'])
    else:
        form.setProjectNumber(context['project_no'])

    for x in dir(form):
       print x

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

#    form.setPenApple(context['deliverables'])
#    form.setTest2("test")
#    form.setRemakrsColumn(context['remarks_column'])
#    form.setItemData(context['item_data'])

    form.createObject().save('/tmp/.tmp.pdf')
    with open('/tmp/.tmp.pdf', 'r') as f:
        return f.read()
    ## ここはちゃんと動作する？要確認
    haru.close()
    f.close()
