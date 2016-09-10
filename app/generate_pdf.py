#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import os, sys
from libharu import *

def lambda_handler(event, context):
    haru    = Libharu()
    haru.open().page_setsize(HPDF_PAGE_SIZE_A4, HPDF_PAGE_PORTRAIT).mbEnable('JP')

    haru.save('/tmp/.tmp.pdf')
    haru.close()
    return "ok"
