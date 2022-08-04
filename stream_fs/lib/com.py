#! /usr/bin/env python
# -*- coding=utf-8 -*-
from lib import *


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()

    return ip


class Mysql(object):

    @staticmethod
    def open(cursor):
        POOL = Config.PYMYSQL_POOL
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


class Redis:
    def __init__(self, db=redis_opt['db']):
        _pool = redis.ConnectionPool(host=redis_opt['host'], port=int(redis_opt['port']), db=int(db),
                                     password=redis_opt['passwd'])
        self._conn = redis.Redis(connection_pool=_pool, decode_responses=True)

    def conn(self):
        return self._conn


def fileinfo(path, file):
    finfo = os.stat(os.path.join(path, file))
    return {'file': file, 'size': size_trf(finfo.st_size), 'lstime': time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(finfo.st_mtime))}


def permissions(self, user):
    rest = self.mysql.fetch_all(tablename='rights', field='archive',
                                condition=f"where role in (select role from roles where user='{user}')")
    return list(map(lambda item: item.get('archive', None), rest))


def transfer_large_files(upload, BASE_DIR):
    '''
    upload: 上传文件对象
    '''
    print('已开启当前cpu数量的线程池:', cpu_)
    # size_ = upload.size
    # print('总文件大小:', size_)
    with open(os.path.join(BASE_DIR, upload['filename']), 'wb') as local:
        print('本地存储路径为:', os.path.join(BASE_DIR, upload['filename']))
        # one_pice = size_ // cpu_  # 每份读写指针大小
        one_pice = 1024 * 1024
        print('每个线程处理的文件大小:', one_pice)
        for i in range(cpu_):
            TP.apply(func=write_slice_file, args=(
                upload, local, i * one_pice, (i + 1) * one_pice, i + 1))
    print('文件写完...')


def size_trf(size):
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    if size <= 0:
        return 0
    for unit in units:
        if size >= 1024:
            size //= 1024
        else:
            size_h = '{} {}'.format(size, unit)
            return size_h

    size_h = '{} {}'.format(size, unit)
    return size_h


def write_slice_file(upload, local, start_pos, end_pos, i):
    '''
    upload: 上传文件对象
    local: 本地存储文件对象
    start_pos: 切片起点
    end_pos: 切片终点
    i: 读取最终校验
    '''
    print('线程开始工作, 启动读写位置:[%s] 终止读写位置:[%s] 当前线程位置:[%s]' %
          (start_pos, end_pos, i))
    upload['body'].seek(start_pos, 0)  # 移动远程读取文件的读写指针位置
    if i != cpu_:
        data = upload.read(end_pos - start_pos)
    else:
        data = upload.read()  # 最后一个线程工作
    local.write(data)
