
# coding:utf-8
import os
import pymysql
from datetime import timedelta,datetime
from DBUtils.PooledDB import PooledDB
from .config import Config

mysql_conf = Config("mysql")


class ConfigMysql(object):
    DEBUG = True
    SECRET_KEY = "umsuldfsdflskjdf"
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=20)
    SESSION_REFRESH_EACH_REQUEST = True
    SESSION_TYPE = "redis"
    config = {
        'creator': pymysql,
        'host': mysql_conf.get('host'),
        'port': int(mysql_conf.get('port')),
        'user': mysql_conf.get('user'),
        'password': mysql_conf.get('passwd'),
        'db': mysql_conf.get('db'),
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




class Mysql(object):

    @staticmethod
    def open(cursor):
        POOL = ConfigMysql.PYMYSQL_POOL
        conn = POOL.connection()
        cursor = conn.cursor(cursor=cursor)
        return conn, cursor

    @staticmethod
    def close(conn, cursor):
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def insert_many(cls, tablename, col_list, value_list, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        sql = f"INSERT INTO {tablename} ({','.join(col_list)}) VALUES ({','.join(['%s' for col in col_list])})"
        row_changes = cursor.executemany(sql, value_list)
        cls.close(conn, cursor)
        return row_changes

    @classmethod
    def fetch_all(cls, tablename, field='*', condition=None, cursor=pymysql.cursors.DictCursor):
        conn, cursor = cls.open(cursor)
        sql = f" SELECT {field} FROM {tablename}  {condition}"
        cursor.execute(sql)
        obj = cursor.fetchall()
        cls.close(conn, cursor)
        return obj