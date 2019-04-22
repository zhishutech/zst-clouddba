
import traceback
import logging

from .base_handler import BaseHandler
from tornado.web import asynchronous
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from opers.mysqlcnf_opers import MysqlcnfOpers


class GenMysqlcnfHandler(BaseHandler):

    executor = ThreadPoolExecutor(5)

    @asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_request_body()
            logging.info('self body from interface /api/v1/mysqlcnf/gen: %s' % str(self.body))
            self.mysqlcnf_opers =  MysqlcnfOpers()
            yield self.do()
            self.finish({'memory':'',  "message": "successful"})
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            self.finish({'memory':error_msg,  "message": "failed"})

    @run_on_executor
    def do(self):
        return self.mysqlcnf_opers.gen()