#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import os, sys
import libharu

def lambda_handler(event, context):
    haru    = libharu.LibHaru()
    haru.open().page_setsize( libharu.HPDF_PAGE_SIZE_A4,
                              libharu.HPDF_PAGE_PORTRAIT ).mbEnable('JP')

    haru.save('/tmp/.tmp.pdf')
    with open('/tmp/.tmp.pdf', 'r') as f:
        return f.read()
    ## ここはちゃんと動作する？要確認
    haru.close()
    f.close()
