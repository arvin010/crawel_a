# coding:utf-8
import os
import pymysql,redis
from datetime import timedelta
from DBUtils.PooledDB import PooledDB



#配置
setting = {
    'autoreload':True,
    'static_path': os.path.join(os.path.dirname(__file__), 'static'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    "cookie_secret":    "base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)",
    "login_url": "/login",
    'xsrf_cookies': False,
    'jwt_expire': 'timedelta(days=30, hours=0, minutes=0, seconds=0)',
    'secret_key' : '.nTG5yS^*.$V7c3ow=#8f7.92c41*&^%de5c.',
    'debug': True,
    'log_file_prefix': "tornado.log",
    'HomePath':'G:\\fs\\',
    'upload_path':"upload"
}

SECRET_KEY = '.689PL$BNVATM'


mysql_opt = dict(
    host="10.142.145.185",
    port=3306,
    db="doc",
    user="root",
    passwd="dccadmin@#",
    charset="utf8",
)

# redis的配置参数
redis_opt = dict(
    host="10.142.145.185",
    port="6379",
    passwd= "dccadmin#",
    db=15
)

class Config(object):
    DEBUG = True
    SECRET_KEY = "umsuldfsdflskjdf"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
    SESSION_REFRESH_EACH_REQUEST = True
    SESSION_TYPE = "redis"
    config = {
        'creator': pymysql,
        'host': mysql_opt['host'],
        'port': mysql_opt['port'],
        'user': mysql_opt['user'],
        'password': mysql_opt['passwd'],
        'db': mysql_opt['db'],
        'maxconnections': 3,
        'cursorclass': pymysql.cursors.DictCursor,
        'mincached': 2,
        'maxcached': 5,
        'maxshared': 3,
        'blocking': True,
        'maxusage': None,
        'setsession': [],
        'ping': 0
    }
    PYMYSQL_POOL = PooledDB(**config)

app_opt= {
    'host':'0.0.0.0',
    'port':8600,
}

# log日志的文件路径
log_file = os.path.join(os.path.dirname(__file__), 'logs/log')
log_level = 'warning'
