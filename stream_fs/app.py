from tornado import web, httpserver, options, ioloop
from config import *
from handles.handles import *

class Applications(web.Application):
    def __init__(self, *arg, **kwargs):
        super(Applications,self).__init__(*arg, **kwargs)

class Serverd():
    def __init__(self):
        self._start()

    def _start(self):
        port=int(app_opt['port'])
        host=app_opt['host']
        print("\033[1;33m*** run time... {} \033[0m".format(time.ctime()))
        print("\033[1;33m*** run {}:{}  \033[0m".format(get_host_ip(), app_opt['port']))
        options.parse_command_line()
        app = Applications(
            routes, **setting
        )
        httpServer = httpserver.HTTPServer(app)
        httpServer.bind(port,address=host)
        httpServer.start()
        ioloop.IOLoop.current().start()

if __name__=="__main__":
    Serverd()
