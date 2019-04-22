#-*- coding: utf-8 -*-

import json
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def get_params(self):
        params = {}
        args = self.request.arguments
        for k in args:
            params[k] = args[k][0]
        return params

    def get_request_body(self):
        args = self.request.body
        if args:
            return json.loads(args)
        else:
            return {}

    def gen_ret_msg(self, records, msg="", code=200):
        if not isinstance(records, list):
            records = [records]
        
        return {"records":records, "msg":msg, "code":code}