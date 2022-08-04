# -*- coding: utf-8 -*-
# @Author: SZW201208
# @Date:   2022-01-20 17:15:28
# @Last Modified by:   SZW201208
# @Last Modified time: 2022-01-20 17:17:41
from handles.syss.syss import *


syss_route=[
    # syss
    url(r'/?',IndexHandler),
    url(r'/filelist/?',IndexHandler),
    url(r"/login/?", Login),
    url(r"/logout/?", Logout),
    url(r"/downloadfile/(?P<filename>.+)?", DownLoadFile),
    url(r"/uploadfiles/?(?P<directory>.+)?", UploadFiles),
    url(r"/upload_success/?(?P<directory>.+)?", Merge),
    url(r"/createdir/?(?P<directory>.+)?", CreateDir),

]