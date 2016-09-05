#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import falcon

class HelloResource(object):

    def on_get(self, req, resp):
        print(req.headers)
        print(req.params)
        print(req.cookies)
        resp.status = falcon.HTTP_200
        resp.content_type = 'text/html'
    
        f = open("sample.html", 'r')
        resp.body = f.read()
        f.close()

class PdfGenerator(object):

    def on_post(cls, req, resp):
        print(req.headers)
        print(req.cookies)
        print(req.stream.read().decode('utf-8'))
        resp.status = falcon.HTTP_200
        resp.body = req.stream.read().decode('utf-8')

app = falcon.API()
falcon.RequestOptions = True
app.add_route("/", HelloResource())
app.add_route("/pdfgen", PdfGenerator())

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server("192.168.1.5", 8000, app)
    httpd.serve_forever()

