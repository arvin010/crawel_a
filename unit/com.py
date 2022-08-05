# coding:utf-8
import os
from datetime import timedelta,datetime


def copy_dir(src_path, target_path):
    if os.path.isdir(src_path) and os.path.isdir(target_path):
        filelist_src = os.listdir(src_path)
        for file in filelist_src:
            path = os.path.join(os.path.abspath(src_path), file)
            if os.path.isdir(path):
                path1 = os.path.join(os.path.abspath(target_path), file)
                if not os.path.exists(path1):
                    os.mkdir(path1)
                copy_dir(path, path1)
            else:
                with open(path, 'rb') as read_stream:
                    contents = read_stream.read()
                    path1 = os.path.join(target_path, file)
                    with open(path1, 'wb') as write_stream:
                        write_stream.write(contents)
        return True

    else:
        return False

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



def str2datetime(str):
    # str = '16-8-2018'
    date_object = datetime.strptime(str, '%d-%m-%y')
    return date_object


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

    # 当期日期属于周几
    week_day=int(now_time.isocalendar()[2])
    # 当前日期所在周的周日

    week_end_time = week_start_time + timedelta(days=6, hours=23, minutes=59, seconds=59)
 
    # 当前日期处于本月第几周
    week_num = int(now_time.strftime('%W')) - int(one_time.strftime('%W')) + 1
 
    # 当前所处月份
    month_num = int(now_time.strftime('%m'))
 
    # 当前年份
    year_num = int(now_time.strftime('%Y'))
    return {'week_start_day':week_start_day,'week_num':week_num,'one_time':one_time,"week_day":week_day}
