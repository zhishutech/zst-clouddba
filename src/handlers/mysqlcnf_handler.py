
import traceback
import logging

from .base_handler import BaseHandler
#from tornado.web import asynchronous
from tornado.gen import coroutine
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor

from opers.mysqlcnf_opers import MysqlcnfOpers

class GenMysqlcnfHandler(BaseHandler):

    executor = ThreadPoolExecutor(5)


    #@asynchronous
    @coroutine
    def post(self):
        try:
            self.body = self.get_params()
            # print(self.body)
            logging.info('self body from interface /api/v1/mysqlcnf/gen: %s' % str(self.body))
            self.mysqlcnf_opers =  MysqlcnfOpers(self.body)
            file_ret = yield self.do()
            self.download(file_ret)
        except:
            error_msg = str(traceback.format_exc())
            print(error_msg)
            self.finish({'memory':error_msg,  "message": "failed"})

    @run_on_executor
    def do(self):
        return self.mysqlcnf_opers.gen()


    def download(self,file_ret):
        # 下载文件
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename="my.cnf.txt"')
        with open(file_ret, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                self.write(data)
        self.finish()
