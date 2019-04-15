#-*- coding: utf-8 -*-

"""common tools classes or functions"""

import threading
import subprocess
import time


class FuncThread(threading.Thread):
    def __init__(self, func, *params, **paramMap):
        super(FuncThread, self).__init__()
        self.func = func
        self.params = params
        self.paramMap = paramMap
        self.rst = None
        self.finished = False

    def run(self):
        self.rst = self.func(*self.params, **self.paramMap)
        self.finished = True

    def get_result(self):
        return self.rst

    def is_finished(self):
        return self.finished


def do_in_thread(func, *params, **kwargs):
    ft = FuncThread(func, *params, **kwargs)
    ft.start()
    return ft


def create_process(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read()
    status = p.wait()
    return status, result


def get_file(filename, mode='r'):
    f = open(filename, mode)
    data = f.read()
    f.close() 
    return data


def set_file(filename, mode, data): 
    f = open(filename, mode)
    f.write(data)
    f.close()


def handle_timeout(func, timeout, *args, **kwargs):
    """do something in some time, check if get result during that and return
    default interval is 1 second
    if define interval, use (timeout, interval)
    
    e.g.
    import time
    def test(m):
        time.sleep(10)
    1: handle_timeout(do_someting, 10, 123)
    2: handle_timeout(do_someting, (10, 2), 123)
    """
    
    interval = 1
    if type(timeout) == tuple:
        timeout, interval = timeout
    rst = None
    while timeout > 0:
        t = time.time()
        rst = func(*args, **kwargs)
        if rst:
            break
        time.sleep(interval)
        timeout -= time.time() - t
    return rst