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

    async def insert(self, tablename, col_list, value_list,):
        
        async with self.pool.acquire() as conn: #从空闲池获取连接的协程。根据需要创建新连接，并且池的大小小于maxsize。
            async with conn.cursor() as cur:
                sql = f"INSERT INTO {tablename} ({','.join(col_list)}) VALUES ({','.join(['%s' for col in col_list])})"
                await cur.execute(sql)
                # print(cur.description)
                row_changes = await cur.executemany()
                return row_changes
                

    # def insert_many(cls, tablename, col_list, value_list, cursor=pymysql.cursors.DictCursor):
    #     conn, cursor = cls.open(cursor)
    #     sql = f"INSERT INTO {tablename} ({','.join(col_list)}) VALUES ({','.join(['%s' for col in col_list])})"
    #     # G.mlog.info(f" [mysql][ insert_many] executed sql : {sql} , value_list: {value_list}")  
    #     row_changes = cursor.executemany(sql, value_list)
    #     cls.close(conn, cursor)
    #     return row_changes
    
    async def close_p(self):
        self.pool.close() # 连接池关闭
        await self.pool.wait_closed() #等待释放和关闭所有已获取连接的协同程序。应该在close（）之后调用，以等待实际的池关闭。
    
    def __del__(self):
        self.loop.run_until_complete(self.close_p())

    # async def main():  # 调用方
    #     tasks = [test_select(), test_update()]  # 把所有任务添加到task中
    #     done, pending = await asyncio.wait(tasks)  # 子生成器
    #     for r in done:  # done和pending都是一个任务，所以返回结果需要逐个调用result()
    #         # print('协程无序返回值：'+r.result())
    #         print(r.result())

    def excute(self,excute_type: str=None):

        self.loop.run_until_complete(eval(f"self.{excute_type}")(excute_type="insert"))


if __name__=="__main__":
    p=Mysql_Pool()
    p.excute(excute_type="insert",)



