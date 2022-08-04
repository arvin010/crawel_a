# -*- coding: utf-8 -*-
# @Author: SZW201208
# @Date:   2021-08-11 09:35:38
# @Last Modified by:   SZW201208
# @Last Modified time: 2022-01-20 17:20:29
#!/usr/bin/env python
# coding=utf-8
from handles import *
from handles.syss.route import *


# routes=[
#     url(r'/?',IndexHandler),
#     url(r'/filelist/?',IndexHandler),
#     url(r"/login/?", Login),
#     url(r"/logout/?", Logout),
#     url(r"/downloadfile/(?P<filename>.+)?", DownLoadFile),
#     url(r"/uploadfiles/?(?P<directory>.+)?", UploadFiles),
#     url(r"/upload_success/?(?P<directory>.+)?", Merge),
#     url(r"/createdir/?(?P<directory>.+)?", CreateDir),
# ]

routes.extend(syss_route)