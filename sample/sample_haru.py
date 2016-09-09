#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import falcon
import os, sys
from ctypes import *

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, '../app'))

from haru import *
from haru.c_func import *
from haru.hpdf_errorcode import *

@HPDF_Error_Handler(None, HPDF_UINT, HPDF_UINT, c_void_p)
def error_handler (error_no, detail_no, user_data):
    global pdf
    printf ("ERROR: %s, detail_no=%u\n", error_detail[error_no],
                detail_no)
    HPDF_Free (pdf)
    sys.exit(1)

## PDF link open test ##
## libharuにてデータストリームを開くテスト用メソッド
class pdf_stream_link_open_test(object):

    def on_get(cls, req, resp):
        print(req.headers)

        global pdf 
        pdf = HPDF_New (error_handler, NULL)
        if (not pdf):
            printf ("error: cannot create PdfDoc object\n")
            return 1

        # JPEncoding
        HPDF_UseJPEncodings (pdf)
        HPDF_UseJPFonts (pdf)

        # create default-font
        font = HPDF_GetFont (pdf, "Helvetica", NULL)

        # add a new page object.
        page = HPDF_AddPage (pdf)

        # A4 size
        HPDF_Page_SetSize (page, HPDF_PAGE_SIZE_A4, HPDF_PAGE_PORTRAIT)
        HPDF_SetPageMode (page, HPDF_PAGE_MODE_FULL_SCREEN)

        # 72dpi A4 size : width x height = 847 x 595
        page_x = 595
        page_y = 820
    
        HPDF_Page_SetFontAndSize (page, font, 10)

        HPDF_SaveToFile(pdf, '/tmp/.tmp.pdf')
        with open('/tmp/.tmp.pdf', 'r') as f:
            resp.body = f.read()
        resp.status = falcon.HTTP_200
        resp.content_type = "application/pdf"

class HelloResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        f = open(os.path.join(path, "sample.html"), 'r')
        resp.body = f.read()
        f.close()

app = falcon.API()
falcon.RequestOptions.auto_parse_form_urlencoded = True
app.add_route("/", HelloResource())
app.add_route("/stream_link_open", pdf_stream_link_open_test())

if __name__ == "__main__":

    from wsgiref import simple_server
    httpd = simple_server.make_server("192.168.33.13", 8000, app)
    httpd.serve_forever()

