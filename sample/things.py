#!/bin/env python
# -*- coding: utf-8 -*-
# vim:set ts=4 sw=4 expandtab fenc=utf-8:
#

import falcon

class HelloResource(object):

    def on_get(self, req, resp):
        resp.body = "test message"
        resp.status = falcon.HTTP_200

app = falcon.API()
app.add_route("/", HelloResource())

if __name__ == "__main__":
    from wsgiref import simple_server
    httpd = simple_server.make_server("192.168.33.13", 8000, app)
    httpd.serve_forever()

