import json
import logging
import subprocess
from socket import *
from util.com import *
from util.config import Config


logging.basicConfig(filename="train_log", format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S ',
                    level=logging.INFO)
logger = logging.getLogger()
KZT = logging.StreamHandler()
KZT.setLevel(logging.DEBUG)
logger.addHandler(KZT)


class SuperBrowser(object):
    # 基础配置
    config = Config("config")
    # 获取业务类型
    business_type = config.get('business_type')
    logger.info("business_type: %s" % business_type)

    # 指定使用英语
    LANGUAGE = config.get('language')

    # ----------------------------------------->> Socket通信地址端口
    host = config.get('socket_host')
    port = int(config.get('socket_port'))
    logger.info('socket > host: %s, port: %s' % (host, port))
    # ----------------------------------------->> 请求紫鸟超级浏览器API方法
    GET_BROWSER_LIST = "getBrowserList"  # 获取店铺列表
    START_BROWSER = "startBrowser"  # 启动店铺(主程序)
    STOP_BROWSER = "stopBrowser"  # 关闭店铺窗口
    GET_BROWSER_ENV_INFO = "getBrowserEnvInfo"  # 启动店铺(webdriver)
    HEARTBEAT = "heartbeat"  # 非必要接口，只是用于保活Socket连接
    EXIT = "exit"  # 正常退出超级浏览器主进程，会自动关闭已启动店铺并保持店铺cookie等信息。

    def __init__(self):
        logger.info("初始化Socket连接...")
        logger.info("启动紫鸟浏览器......")

        self.buf_size = int(self.config.get('socket_buf_size'))
        self.IS_HEADLESS = self.config.get('browser_is_headless')  # 浏览器是否启用无头模式 false 否、true 是

        # 获取紫鸟·超级浏览器安装路径
        path_super_browser = self.config.get('path_super_browser')
        cmd = "{} --run_type=web_driver --socket_port={}".format(path_super_browser, self.port)
        subprocess.Popen(cmd)

        try:
            # ------------------------------创建套接字通道
            self.address = (self.host, self.port)
            self.tcpCliSock = socket(AF_INET, SOCK_STREAM)  # 创建套接字
            self.tcpCliSock.connect(self.address)  # 主动初始化TCP服务器连接
        except ConnectionRefusedError as e:
            logger.error(e)
            subprocess.Popen('taskkill /f /im superbrowser.exe')
        except Exception as e:
            logger.error(e)

    def browser_api(self, action, args=None):
        """
        紫鸟·超级浏览器API
        :param action: 方法
        :param args: 可选参数
        :return:
        """
        REQUEST_ID = "0123456789"  # 全局唯一标识
        user_info = json.dumps({  # 用户信息
            "company": self.config.get('browser_company_name'),
            "username": self.config.get('browser_username'),
            "password": self.config.get('browser_password')
        })

        # cdm默认为获取店铺列表
        common = {"userInfo": user_info, "action": self.GET_BROWSER_LIST, "requestId": REQUEST_ID}
        if action == self.START_BROWSER or action == self.GET_BROWSER_ENV_INFO or action == self.STOP_BROWSER:
            common['browserOauth'] = args['browserOauth']
            common['isHeadless'] = args['isHeadless']
        if action == self.START_BROWSER:
            common['launcherPage'] = "https://sellercentral.amazon.co.uk"
            common['runMode'] = "1"
        common['action'] = action
        return common

    def socket_communication(self, params):
        """
        Socket通信
        :param params: 参数对象
        :return:
        """
        try:
            args = (str(params) + '\r\n').encode('utf-8')
            # 将 string 中的数据发送到连接的套接字
            self.tcpCliSock.send(args)
            # 接收的最大数据量
            res = self.tcpCliSock.recv(self.buf_size)
            return json.loads(res)
        except ConnectionResetError as e:
            logger.warning("ConnectionResetError: %s" % e)
            logger.info("socket 连接已关闭")
        except Exception as e:
            logger.error("socket_communication error: %s" % e)
        pass


if __name__=="__main__":
    brow=SuperBrowser()