#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#
import falcon
import os, sys, json

path = os.path.dirname(__file__)
sys.path.append(os.path.join(path, '../app/'))

from generate_pdf import *

def before_resource(req, resp, resource, params):
    print('Headers : ' + str(req.headers))
    print("Params  : " + str(req.params))
    print("Cookies : " + str(req.cookies))
    # if req.method == 'POST':
        # print("Body    : " + req.stream.read().decode('utf-8'))

@falcon.before(before_resource)
class HelloResource(object):

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
        f = open(os.path.join(path, "sample.html"), 'r')
        resp.body = f.read()
        f.close()

@falcon.before(before_resource)
class PdfGenerator(object):

    def on_post(cls, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = "application/pdf"

        event = { "test" : "test", "hoge" : "hoge" }
        resp.body = lambda_handler(event, json.loads(req.stream.read().decode('utf-8')))

app = falcon.API()
falcon.RequestOptions.auto_parse_form_urlencoded = True
app.add_route("/", HelloResource())
app.add_route("/generate", PdfGenerator())

if __name__ == "__main__":

    from wsgiref import simple_server
    httpd = simple_server.make_server("192.168.33.13", 8000, app)
    httpd.serve_forever()

