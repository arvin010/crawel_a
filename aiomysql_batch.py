#!/usr/bin/env python3
# coding: utf-8

import time
import asyncio
import aiomysql

start = time.time()
loop = asyncio.get_event_loop()

async def test_example():
    conn = await aiomysql.connect(host='192.168.31.230', port=3306,
                                       user='root', password='abcd1234',
                                       db='test', loop=loop)

    # create default cursor
    cursor = await conn.cursor()

    # execute sql query
    data = []
    for i in range(1,30000):
        data.append(('xiao%s'%i, '123', '12345678910', '123@qq.com', '2020-04-10 01:22:07'),)

    stmt = "INSERT INTO users (username,password,phone,email,create_time) VALUES(%s,%s,%s,%s,%s);"

    await cursor.executemany(stmt, data)
    await conn.commit()
    # detach cursor from connection
    await cursor.close()

    # close connection
    conn.close()

loop.run_until_complete(test_example())
print('所有IO任务总耗时%.5f秒' % float(time.time() - start))