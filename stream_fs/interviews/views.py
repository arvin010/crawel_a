from interviews import *
from pathconfig import*


class DownLoadFile(RequestHandler):
    @authenticated
    async def post(self, filename=None):
        try:
            path = ''
            for i in [self.application.settings['HomePath'], self.application.settings['upload_path'], filename.strip()]:
                path = os.path.join(path, i)
            if not os.path.isdir(path) and self.request.headers.get('user', None):
                self.mysql.insert_many(tablename='logs', col_list=['file', 'operator'], value_list=[[path.split(
                    self.application.settings["upload_path"], 1)[-1], self.request.headers.get('user', None)]])
                self.set_header('Content-Type', 'application/octet-stream')
                # self.set_header('Content-Length',str(os.stat(path).st_size))
                # self.set_header('Content-Disposition', 'attachment; filename='+filename)
                # async with aiofile.async_open(path, 'rb') as f:
                #    reader = aiofile.Reader(aio_file=f)
                #    async for data in reader:
                #         self.write(data)
                #         self.flush()
                with open(path, 'rb') as f:
                    # while True:
                    f.seek(int(self.request.headers.get('start', 0)), 0)
                    data = f.read(
                        int(self.request.headers.get('chunkSize', 0)))
                    # if not data:
                    # break
                    self.write(data)
        except Exception as e:
            print(traceback.format_exc())
        finally:
            self.finish()

    @authenticated
    def get(self, filename=None):
        path = ''
        filed = ['公共']
        for i in [self.application.settings['HomePath'], self.application.settings['upload_path']]:
            if i:
                path = os.path.join(path, i.strip()).lower()
        if filename:
            path = os.path.join(path, filename)
            if not os.path.isdir(path):
                self.set_header('ContentLength', str(os.stat(path).st_size))
                return self.write(json.dumps({"Result": False, "Message": "file"}))
            else:
                files = os.listdir(path)
                files = list(map(lambda f: fileinfo(path, f), files))
                parent = path.split(
                    f'{self.application.settings["upload_path"]}', 1)[-1]
                parent = parent if not parent else parent[1:]
        else:
            files = list(map(lambda f: fileinfo(path, f), permissions(
                self, self.decrypt(self.get_cookie('usern'))) + filed))
            parent = ''
        files = sorted(files, key=lambda f: (
            f['lstime'], f['file']), reverse=True)
        return self.write(json.dumps({"Result": True, "Message": "filelist", "Content": files, "parent": parent}))


class Login(RequestHandler):
    resdata = {"result": False, "message": 'succeeful'}

    def post(self):
        _params = json.loads(self.request.body.decode('utf-8'))
        self.user = _params.get("username", None)
        if self.user:
            self.user.lower()
        self.ip = self.request.headers.get(
            'remote_ip', None) if not self.request.remote_ip else self.request.remote_ip
        self.passwd = _params.get("pwd", None)
        if self.authentic():
            subPath = ['1']
            self.write(json.dumps({"Result": True, "Message": "succeed:"}))
            self.set_secure_cookie('user', self.generate_token(
                isremember=True, username=self.user, passwd=self.passwd))
            self.set_secure_cookie('role', '1')
        else:
            self.write(json.dumps(
                {"Result": False, "Message": "authentic failed"}))

    def get(self):
        self.set_secure_cookie('user', '')
        self.render('login.html')


class Logout(RequestHandler):
    @authenticated
    def get(self):
        self.set_secure_cookie('user', '')
        self.write(json.dumps({"Result": True, "Message": "succeessfull"}))


class IndexHandler(RequestHandler):
    @authenticated
    def get(self):
        # try:
        if self.current_user:
            path = ""
            totalPath = [self.application.settings['HomePath'],
                         self.application.settings['upload_path']]
            for i in totalPath:
                path = os.path.join(path, i).lower()
            files = os.listdir(path)
            self.render('file-list.html', result=files)
        else:
            self.render('login.html')
        # except Exception:
        #     self.write(json.dumps({"Result": False, "Message": "New task failed:" + str(traceback.format_exc())}))


class UploadFiles(RequestHandler):
    resdata = {"result": False, "message": 'succeeful'}

    @authenticated
    async def post(self, directory, *args, **kwargs):
        try:
            upload_path = ""
            for i in [self.application.settings['HomePath'], self.application.settings['upload_path'], 'tmp']:
                upload_path = os.path.join(upload_path, i).lower()
            task = self.get_argument('task_id', 0)  # 获取文件的唯一标识符
            chunk = self.get_argument('chunk', 0)  # 获取该分片在所有分片中的序号
            filename = '%s%s' % (task, chunk)  # 构造该分片的唯一标识符
            upload_file = self.request.files
            with open(os.path.join(upload_path, filename), 'wb') as up:
                up.write(upload_file['file'][0]['body'])
            # file_metas = self.request.files['file'][0]
            # print(file_metas.keys())
            # filename = file_metas['filename']
            # if filename not in os.listdir(upload_path):
            #     transfer_large_files(file_metas,upload_path)
            #     # filepath = os.path.join(upload_path, filename)
            #     # with open(filepath, 'wb') as up:
            #     #     up.write(file_metas[0]['body'])
            #     self.resdata={"result": True, "message": 'succeeful','data':fileinfo(upload_path,filename)}
            # else:
            #     self.resdata={"result": True, "message": '文件已存在'}
            # else:
            #     self.resdata={"result": True, "message": '该目录下不允许操作'}
        except Exception as e:
            print(traceback.format_exc())
            self.resdata['Message'] = str(traceback.format_exc())
        finally:
            self.write(json.dumps(self.resdata, default=str))


class Merge(RequestHandler):
    resdata = {"result": False, "message": 'succeeful'}

    @authenticated
    async def post(self, directory, *args, **kwargs):
        try:
            upload_path = ""
            parent = self.get_argument('parent', None)
            if parent:
                base_path = os.path.join(
                    self.application.settings['HomePath'], self.application.settings['upload_path']).lower()
                upload_path = os.path.join(base_path, parent)
                tmp_path = os.path.join(base_path, 'tmp')
                # file_metas = self.request.files['file'][0]
                # filename = file_metas['filename']
                target_filename = self.get_argument('filename')  # 获取上传文件的文件名
                if target_filename not in os.listdir(upload_path):
                    task = self.get_argument('task_id')  # 获取文件的唯一标识符
                    chunk = 0  # 分片序号
                    with open(os.path.join(upload_path, target_filename), 'wb') as target_file:  # 创建新文件
                        while True:
                            try:
                                filename = os.path.join(
                                    tmp_path, f'{task}{chunk}')
                                source_file = open(filename, 'rb')  # 按序打开每个分片
                                target_file.write(
                                    source_file.read())  # 读取分片内容写入新文件
                                source_file.close()
                            except IOError as msg:
                                break

                            chunk += 1
                            os.remove(filename)  # 删除该分片，节约空间
                    # transfer_large_files(file_metas,upload_path)
                    # filepath = os.path.join(upload_path, filename)
                    # with open(filepath, 'wb') as up:
                    #     up.write(file_metas[0]['body'])
                    self.resdata = {"result": True, "message": 'succeeful', 'data': fileinfo(
                        upload_path, target_filename)}
                else:
                    self.resdata = {"result": True, "message": '文件已存在'}
            else:
                self.resdata = {"result": True, "message": '该目录下不允许操作'}
        except Exception as e:
            self.resdata['Message'] = str(traceback.format_exc())
        finally:
            self.write(json.dumps(self.resdata, default=str))


class CreateDir(RequestHandler):
    resdata = {"result": False, "message": 'succeeful'}

    @authenticated
    async def post(self, directory):
        try:
            _params = json.loads(self.request.body.decode('utf-8'))
            upload_path = ""
            if directory:
                for i in [self.application.settings['HomePath'], self.application.settings['upload_path'], directory]:
                    upload_path = os.path.join(upload_path, i).lower()
                if _params.get('dir', None) and _params['dir'] not in os.listdir(upload_path):
                    os.makedirs(os.path.join(upload_path, _params['dir']))
                    self.resdata = {"result": True, "message": 'succeeful', 'data': fileinfo(
                        upload_path, _params['dir'])}
                else:
                    self.resdata = {"result": True, "message": '文件夹已存在'}
            else:
                self.resdata = {"result": True, "message": '该目录下不允许操作'}
        except Exception as e:
            self.resdata['Message'] = str(e)
        finally:
            self.write(json.dumps(self.resdata, default=str))
