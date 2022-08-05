from util.Database import Database
from util.ConfigUtil import Config
from core.CoreThread import CoreThread
import time
import datetime
from random import *


class StartCore():
    __max_tharead_number = 0
    __idle_tharead_number = 0
    __busy_tharead_number = 0
    __tharead_data = []
    max_run_time = 60 * 0.5

    def __init__(self, max_tharead_number=None):
        self.config = Config()
        self.__linkDb()
        if max_tharead_number == None:
            self.__max_tharead_number = int(self.config.getThreadConfig('max_keywords_thread'))
        else:
            self.__max_tharead_number = int(max_tharead_number)

    def __linkDb(self):
        self.db = Database(
            host=self.config.getMysqlConfig('host'),
            user=self.config.getMysqlConfig('user'),
            password=self.config.getMysqlConfig('password'),
            db=self.config.getMysqlConfig('db'),
        )

    def getClientStartState(self):
        sql = "select id from customer where state = %s and is_del = %s and monitoring_state = %s"
        result = self.db.select(sql, data=(0, 0, 0))
        client_id_list = {}
        if len(result) > 0:
            for val in result:
                client_id_list[val[0]] = {
                    'client_id': val[0],
                }
        return client_id_list

    def getKeywordsAuto(self, client_id_list):
        result = []
        if len(client_id_list) > 0:
            sql = 'select a.id,a.keywords,b.cookie,b.uuid,b.latitude,b.longitude,a.max_price,a.min_price,a.client_id,a.auto_create_shopping_car,b.default_addr_id,a.time_where from keywords as a left join operation_user as b on a.operation_user_id = b.id where a.is_del=%s and (a.state in %s or (a.state = 1 and (UNIX_TIMESTAMP(now()) - UNIX_TIMESTAMP(a.last_start_time)) >= 25)) and error_num < %s and a.client_id in %s order by a.thread_end_time asc limit {}'.format(
                self.__idle_tharead_number)
            result = self.db.select(sql, data=(0, [0, 2, 3], 3, client_id_list))
        return result

    def startAuto(self):
        while True:
            self.__idle_tharead_number = self.__max_tharead_number - len(self.__tharead_data)
            self.__busy_tharead_number = len(self.__tharead_data)

            if self.__idle_tharead_number > 0:
                self.addTask()

            if self.__busy_tharead_number > 0:
                self.cleanTask()

            time.sleep(26)

    def cleanTask(self):
        for task_key, task_obj in enumerate(self.__tharead_data):
            if task_obj.is_alive() == False:
                del self.__tharead_data[task_key]

    def getCrawlUser(self, client_id_list):
        sql = "SELECT id,cookie,uuid,latitude,longitude,client_id FROM operation_user where client_id in %s and user_type=%s and is_del=%s"
        result = self.db.select(sql, data=(client_id_list, 1, 0))
        data_info = {}
        for val in result:
            if (val[5] not in data_info):
                data_info[val[5]] = []
            data_info[val[5]].append({
                'id': val[0],
                'cookie': val[1],
                'uuid': val[2],
                'latitude': val[3],
                'longitude': val[4],
            })
        return data_info

    def addTask(self):
        client_data = self.getClientStartState()
        if len(client_data) > 0:
            client_id_list = list(client_data.keys())
            keywords_data = self.getKeywordsAuto(client_id_list)
            if len(keywords_data) > 0:
                data_info = self.getCrawlUser(client_id_list)
                for keywords_val in keywords_data:
                    info = {
                        'id': keywords_val[0],
                        'keywords': keywords_val[1],
                        'cookie': keywords_val[2],
                        'uuid': keywords_val[3],
                        'latitude': keywords_val[4],
                        'longitude': keywords_val[5],
                        'max_price': keywords_val[6],
                        'min_price': keywords_val[7],
                        'client_id': keywords_val[8],
                        'auto_create_shopping_car': keywords_val[9],
                        'default_addr_id': keywords_val[10],
                        'crawl_user_info': self.randomUser(data_info, keywords_val[8]),
                        'time_where': keywords_val[11]
                    }

                    tk = CoreThread("keywords_id:".format(keywords_val[0]), info, self.max_run_time)
                    self.saveAutoStartData(info['id'])
                    self.__tharead_data.append(tk)
                    tk.start()
            else:
                print("没有要处理的数据")
        else:
            print("没有要处理的数据")

    def saveAutoStartData(self, id):
        data = (1, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), id)
        sql = "update keywords set state=%s,last_start_time=%s where id=%s"
        try:
            self.db.update(sql, data=data)
        except Exception as res:
            self.__linkDb()
            self.db.update(sql, data=data)

    def randomUser(self, data_info, client_id):
        return data_info[client_id][randint(0, len(data_info[client_id])) - 1]

