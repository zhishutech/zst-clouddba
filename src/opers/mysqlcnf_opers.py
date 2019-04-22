# -*- coding: utf-8 -*-
from tornado import web
import configparser
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class MysqlcnfOpers(object):

    def __init__(self, body):
        self.body = body

    def gen(self):
        hostname = str(self.body['hostname'], 'utf-8')
        totalmem = str(self.body['totalmem'], 'utf-8')
        myver = str(self.body['myver'], 'utf-8')
        serarc = str(self.body['serarc'], 'utf-8')
        dedicated = str(self.body['dedicated'], 'utf-8')
        basedir = str(self.body['basedir'], 'utf-8')
        datadir = str(self.body['datadir'], 'utf-8')
        port = str(self.body['port'], 'utf-8')
        socket = str(self.body['socket'], 'utf-8')
        maxtabs = str(self.body['maxtabs'], 'utf-8')
        maxconn = str(self.body['maxconn'], 'utf-8')
        expbinlog = str(self.body['expbinlog'], 'utf-8')
        freqsort = str(self.body['freqsort'], 'utf-8')
        trxlevel = str(self.body['trxlevel'], 'utf-8')

        # print(hostname, totalmem, myver, serarc, dedicated, basedir, datadir, port, socket, maxtabs, maxconn, expbinlog,freqsort, trxlevel)

        file_ret = self.parse(hostname, totalmem, myver, serarc, dedicated, basedir, datadir, port, socket, maxtabs, maxconn,
                         expbinlog, freqsort, trxlevel)

        return (file_ret)


    def parse(self, hostname, totalmem, myver, serarc, dedicated, basedir, datadir, port, socket, maxtabs, maxconn, expbinlog,
              freqsort, trxlevel):
        '''
        处理my.cnf文件，解析替换用户填入的值
        '''
    
        # 模板文件
        example_file = '%s/config/my.cnf.example' % BASE_DIR
        # 解析后的文件
        file_ret = '%s/config/my.cnf.txt' % BASE_DIR
    
        # 判断文件是否存在，存在则删除
        if (os.path.exists(file_ret)):
            os.remove(file_ret)
        conf = configparser.ConfigParser(allow_no_value=True)
        conf.read(example_file, encoding='utf-8')
    
        # 解析替换参数
        prompt = "'\\u@%s \\R:\\m:\\s [\\d]>' " % hostname
        pid_file = "%s.pid" % hostname
        table_cache = str(round(int(maxtabs) * 2))
        slow_query_log_file = '%s/slow_log' % datadir
        log_error = '%s/error.log' % datadir
        log_bin = '%s/mybinlog' % datadir
        thread_cache = str(round(int(maxconn) * 1.5))
        innodb_undo_dir = '%s/undolog' % datadir
        binlog_expire_logs_seconds = str(int(expbinlog) * 60 * 60 * 24)
    
        # 判断filesort是否过多。
        if freqsort == '1':
            sort_buffer_size = '16M'
            join_buffer_size = '16M'
            read_rnd_buffer_size = '16M'
            tmp_table_size = '96M'
        else:
            sort_buffer_size = '4M'
            join_buffer_size = '4M'
            read_rnd_buffer_size = '4M'
            tmp_table_size = '32M'
        # 判断是否是专属数据库服务器，0=否
        if dedicated == '0':
            inno_bp_size = round(int(totalmem) * 1024 * 0.7 * 0.7)
            key_buf = round(32 * 0.7)
        else:
            inno_bp_size = round(int(totalmem) * 1024 * 0.7)
            key_buf = 32
        # 判断系统是32位/64位，0=32位
        if serarc == '0':
            inno_bp_size = 2048
        # if innodb buffer pool great than 64G, then buffer pool instance set to 8, else set to 4
        if inno_bp_size >= 64 * 1024:
            ibp_inst = '8'
        else:
            ibp_inst = '4'
    
        conf.set('client', 'port', port)
        conf.set('client', 'socket', socket)
        conf.set('mysql', 'prompt', prompt)
        conf.set('mysqld', 'port', port)
        conf.set('mysqld', 'basedir', basedir)
        conf.set('mysqld', 'datadir', datadir)
        conf.set('mysqld', 'socket', socket)
        conf.set('mysqld', 'pid-file', pid_file)
        conf.set('mysqld', 'max_connections', maxconn)
        conf.set('mysqld', 'table_open_cache', table_cache)
        conf.set('mysqld', 'table_definition_cache', table_cache)
        conf.set('mysqld', 'sort_buffer_size', sort_buffer_size)
        conf.set('mysqld', 'join_buffer_size', join_buffer_size)
        conf.set('mysqld', 'read_rnd_buffer_size', read_rnd_buffer_size)
        conf.set('mysqld', 'tmp_table_size', tmp_table_size)
        conf.set('mysqld', 'max_heap_table_size', tmp_table_size)
        conf.set('mysqld', 'thread_cache_size', thread_cache)
        conf.set('mysqld', 'slow_query_log_file', slow_query_log_file)
        conf.set('mysqld', 'log_error', log_error)
        conf.set('mysqld', 'log_bin', log_bin)
        conf.set('mysqld', 'server_id', port)
        conf.set('mysqld', 'expire_logs_days', expbinlog)
        conf.set('mysqld', 'key_buffer_size', str(key_buf))
        conf.set('mysqld', 'innodb_buffer_pool_size', str(inno_bp_size) + 'M')
        conf.set('mysqld', 'innodb_buffer_pool_instances', ibp_inst)
        conf.set('mysqld', 'innodb_flush_log_at_trx_commit', trxlevel)
        conf.set('mysqld', 'innodb_undo_directory', innodb_undo_dir)
    
        # 判断数据库版本，57=5.7
        if myver == '57':
            conf.set('mysqld', '\n# some var for MySQL 5.7')
            conf.set('mysqld', 'innodb_checksums', '1')
            conf.set('mysqld', 'query_cache_size', '0')
            conf.set('mysqld', 'query_cache_type', '0')
            conf.set('mysqld', 'innodb_undo_logs', '128')
        else:
            conf.set('mysqld', '\n# some var for MySQL 8.0')
            conf.set('mysqld', 'log_error_verbosity', '3')
            conf.set('mysqld', 'innodb_print_ddl_logs', '1')
            conf.set('mysqld', 'binlog_expire_logs_seconds', binlog_expire_logs_seconds)
            conf.remove_option('mysqld', 'expire_logs_days')
    
        with open(file_ret, 'w') as f:
            conf.write(f)
    
        with open(file_ret, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            if myver == '57':
                f.write(
                    '## my.cnf for MySQL 5.7\n## author: ZST Cloud DBA\n## 知数堂\n## 靠谱优质的在线培训品牌\n## http://www.zhishutang.com/\n## QQ群: 650149401\n## 注意：个别建议可能需要根据实际情况作调整，请自行判断,ZST Cloud DBA不对这些建议结果负相应责任\n## 本配置文件主要适用于MySQL 5.7版本\n\n\n' + content)
            else:
                f.write(
                    '## my.cnf for MySQL 8.0\n## author: ZST Cloud DBA\n## 知数堂\n## 靠谱优质的在线培训品牌\n## http://www.zhishutang.com/\n## QQ群: 650149401\n## 注意：个别建议可能需要根据实际情况作调整，请自行判断,ZST Cloud DBA不对这些建议结果负相应责任\n## 本配置文件主要适用于MySQL 8.0版本\n\n\n' + content)
    
        return file_ret

