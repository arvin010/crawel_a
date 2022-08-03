#!/usr/bin/env python
#-*- coding: utf-8 -*-
import asyncio
import aiomysql


class Mysql_Pool():

    pool=None
    loop = asyncio.get_event_loop()

    def __init__(self):
        self.loop.run_until_complete(self.create_p())

    async def create_p(self):
        self.pool = await aiomysql.create_pool(host='192.168.16.246', port=3306,
                    user='root', password='root',
                    db='bi_db', loop=self.loop) # 创建连接池

    async def insert(self,excute_type : str=None):
        
        async with self.pool.acquire() as conn: #从空闲池获取连接的协程。根据需要创建新连接，并且池的大小小于maxsize。
            async with conn.cursor() as cur:
                await cur.execute("show tables")
                print(cur.description)
                r = await cur.fetchall()
                print(r)
    
    async def close_p(self):
        self.pool.close() # 连接池关闭
        await self.pool.wait_closed() #等待释放和关闭所有已获取连接的协同程序。应该在close（）之后调用，以等待实际的池关闭。
    
    def __del__(self):
        self.loop.run_until_complete(self.close_p())


    def excute(self,excute_type: str=None):

        self.loop.run_until_complete(eval(f"self.{excute_type}")(excute_type="insert"))


if __name__=="__main__":
    p=Mysql_Pool()
    p.excute(excute_type="insert")



