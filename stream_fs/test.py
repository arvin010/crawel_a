# -*- coding: utf-8 -*-
# @Author: SZW201208
# @Date:   2021-12-15 14:21:26
# @Last Modified by:   SZW201208
# @Last Modified time: 2021-12-24 11:13:16
# from django.shortcuts import render
# from django.views import View
# from django.http import HttpResponse
from multiprocessing.pool import ThreadPool
from multiprocessing import cpu_count
from bigfile.settings import BASE_DIR
import os
# Create your views here.

cpu_ = cpu_count()  # 获取当前cpu数量，用以启动一定线程数量的线程池子
TP = ThreadPool(cpu_)

print(TP)


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
    upload.seek(start_pos, 0)  # 移动远程读取文件的读写指针位置
    if i != cpu_:
        data = upload.read(end_pos - start_pos)
    else:
        data = upload.read()  # 最后一个线程工作
    local.write(data)


def transfer_large_files(upload,BASE_DIR):
    '''
    upload: 上传文件对象
    '''
    print('已开启当前cpu数量的线程池:', cpu_)
    print(dir(upload))
    # size_ = upload.size
    print('总文件大小:', size_)
    with open(os.path.join(BASE_DIR, upload.name), 'wb') as local:
        print('本地存储路径为:', os.path.join(BASE_DIR, upload.name))
        # one_pice = size_ // cpu_  # 每份读写指针大小
        one_pice= 1024*1024
        print('每个线程处理的文件大小:', one_pice)
        for i in range(cpu_):
            TP.apply(func=write_slice_file, args=(
                upload, local, i * one_pice, (i+1) * one_pice, i + 1))
    print('文件写完...')


class TB_File(View):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        upload = request.FILES['file']
        transfer_large_files(upload)
        return HttpResponse('OK')












def get_args(self):
    """Return the arguments to be passed after self.cmd
     Doesn't expect shell expansion to happen.
     """
    args = []

    if self.ip:
    args.append('--ip="%s"' % self.ip)

    if self.port:
    args.append('--port=%i' % self.port)
    elif self.server.port:
    self.log.warning("Setting port from user.server is deprecated as of JupyterHub 0.7.")
    args.append('--port=%i' % self.server.port)

    if self.notebook_dir:
    notebook_dir = self.format_string(self.notebook_dir)
    args.append('--notebook-dir="%s"' % notebook_dir)
    if self.default_url:
    default_url = self.format_string(self.default_url)
    args.append('--NotebookApp.default_url="%s"' % default_url)

    if self.debug:
    args.append('--debug')
    if self.disable_user_config:
    args.append('--disable-user-config')
    args.append('--allow-root')
    args.extend(self.args)
    return args





def system_user_exists(self, username):
    """Check if the user exists on the system"""
    try:
        pwd.getpwnam(username)
    except KeyError:
        return False
    else:
        return True

def add_system_user(self, username, password):
    """Create a new local UNIX user on the system.
    Tested to work on FreeBSD and Linux, at least.
    """
    res = os.system('useradd  %(name1)s -s /bin/nologin' % {'name1':username})
    if res:
        self.log.warn('user %s create failure' % username)
        return False

    res = os.system('echo %(pass)s |passwd --stdin %(name1)s' % {'name1': username, 'pass':password})
    if res:
        self.log.warn('user %s password create failure' % username)
        return False

    return True


c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = "ldap://ldap.cmc-xinnuo.com:389"
c.LDAPAuthenticator.lookup_dn = False
c.LDAPAuthenticator.lookup_dn_search_filter = '({login_attr}={login})'
c.LDAPAuthenticator.lookup_dn_search_user = ''
c.LDAPAuthenticator.lookup_dn_search_password = ''
c.LDAPAuthenticator.user_search_base = 'OU=xx,OU=xx,OU=xx,DC=xxx,DC=xx'
c.LDAPAuthenticator.user_attribute = 'sAMAccountName'
c.LDAPAuthenticator.lookup_dn_user_dn_attribute = 'xx'
c.LDAPAuthenticator.bind_dn_template = 'CMC\{username}'



c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = "ldap://ldap.cmc-xinnuo.com:389"
c.LDAPAuthenticator.lookup_dn = False
c.LDAPAuthenticator.lookup_dn_search_filter = '({login_attr}={login})'
c.LDAPAuthenticator.lookup_dn_search_user = 'ldap_search_user_technical_account'
c.LDAPAuthenticator.lookup_dn_search_password = 'secret'
c.LDAPAuthenticator.user_search_base = 'ou=people,dc=cmc-xinnuo,dc=com'
c.LDAPAuthenticator.user_attribute = 'sAMAccountName'
c.LDAPAuthenticator.lookup_dn_user_dn_attribute = 'cn'
c.LDAPAuthenticator.escape_userdn = False
c.LDAPAuthenticator.bind_dn_template = 'CMC\{username}'


c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = 'ldap://ldap.cmc-xinnuo.com:389'
c.LDAPAuthenticator.bind_dn_template = 'CMC\{username}'
c.LDAPAuthenticator.lookup_dn = False
c.LDAPAuthenticator.user_search_base = 'OU=Development,OU=Company Users,DC=cmc-xinnuo,DC=local'
c.LDAPAuthenticator.user_attribute = 'sAMAccountName'
c.LDAPAuthenticator.allowed_groups = []
\



c.Spawner.default_url = '/lab'
# /lab对应jupyterlab 默认为notebook
c.JupyterHub.port = 8888
c.JupyterHub.hub_port =8889
c.JupyterHub.ip='0.0.0.0'
# 指定暴露端口
c.PAMAuthenticator.encoding = 'utf8'
c.Authenticator.whitelist = {'root','admin', 'jupyter', 'aiker','szw201208'}
# 指定可使用用户
c.LocalAuthenticator.create_system_users = True
c.Authenticator.admin_users = {'root', 'admin','szw201208'}
c.DummyAuthenticator.password='root'
# 指定admin用户
c.JupyterHub.statsd_prefix = 'jupyterhub'
c.Spawner.notebook_dir = '/workspace'
#jupyterhub自定义目录
c.Spawner.cmd=['jupyterhub-singleuser']
c.JupyterHub.bind_url='http://0.0.0.0:8888'



c.JupyterHub.authenticator_class = 'ldapauthenticator.LDAPAuthenticator'
c.LDAPAuthenticator.server_address = 'ldap://ldap.xxx.com:389'
c.LDAPAuthenticator.bind_dn_template = 'company\{username}'
c.LDAPAuthenticator.lookup_dn = False
c.LDAPAuthenticator.user_search_base = 'OU=Development,OU=Company Users,DC=company,DC=local'
c.LDAPAuthenticator.user_attribute = 'sAMAccountName'
c.LDAPAuthenticator.allowed_groups = []




