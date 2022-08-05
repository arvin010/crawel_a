from datetime import datetime,timedelta



def get_week(date_str=None):
    if date_str and isinstance(date_str, str):
        now_time = datetime.strptime(date_str + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    else:
        now_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    # 当月第一天
    one_time = now_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # 当前日期所在周的周一
    week_start_time = now_time - timedelta(days=now_time.weekday(), hours=now_time.hour, minutes=now_time.minute,
                                           seconds=now_time.second)
    week_start_day=int(week_start_time.strftime('%d'))
    print(week_start_day)
    # 当前日期所在周的周日
    week_end_time = week_start_time + timedelta(days=6, hours=23, minutes=59, seconds=59)
 
    # 当前日期处于本月第几周
    week_num = int(now_time.strftime('%W')) - int(one_time.strftime('%W')) + 1
    print(week_num)
    # 当前所处月份
    month_num = int(now_time.strftime('%m'))
 
    # 当前年份
    year_num = int(now_time.strftime('%Y'))


t = datetime.now()  # (2020, 16, 7)
y = t.isocalendar()[0] # 2020年
week_count = t.isocalendar()[1] # 第16周
d = t.isocalendar()[2] # 周天
print(d)


get_week('2022-8-16')