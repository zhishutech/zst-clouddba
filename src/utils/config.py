import os
import configparser

base_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
current_dir = os.path.dirname(os.path.abspath(__file__))
server_conf_path = os.path.join(os.path.dirname(current_dir), r'config/server.conf')

conf = configparser.ConfigParser()
conf.read(server_conf_path)

SERVER_PORT = conf.get('server', 'port')