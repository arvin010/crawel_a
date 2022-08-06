from util.db import Mysql





def report_insert_mysql(data):
    
    sql_pool=Mysql()
    sql_pool.insert_many(tablename='report',col_list=['platform','shop','site','rep_type','rep_date_type',"rep_date_start",
                                                "rep_date_end",'save_type','save_dir','is_del_loction'],
                            value_list=[[data["platform"],data["shop"],data['country'],data["report_type"],data["date_type"],data["date_start"],data["date_end"],
                                        data["save_type"],data["save_dir"],data["is_del_loction"]]])