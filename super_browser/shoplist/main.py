import logging

logging.basicConfig(filename="train_log", format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S ',
                    level=logging.INFO)
logger = logging.getLogger()
KZT = logging.StreamHandler()
KZT.setLevel(logging.DEBUG)
logger.addHandler(KZT)

country_list=["US" , "MX", "CA"]  # BR
report_dir={'日期范围报告':1}
platform_dir={1:"amazon",2:"aliexpress"}



def browser_list(self):
    """
    获取店铺列表
    这里采用Redis管理店铺，为了后期分布式部署准备。
    :return:
    {
        "statusCode": "状态码",
        "err": "异常信息",
        "action": "getBrowserList",
        "requestId": "全局唯一标识",
        "browserList": [{
            "browserOauth": "店铺ID",
            "browserName": "店铺名称",
            "browserIp": "店铺IP",
            "siteId": "店铺所属站点",
            "isExpired": false //ip是否过期
        }]
    }
    """
    logger.info("")
    logger.info("获取店铺列表.")
    shop_list_params = self.browser_api("getBrowserList")
    shop_info = self.socket_communication(shop_list_params)
    if shop_info['statusCode'] == 0:
        print(shop_info)
        browser_size = len(shop_info['browserList'])
        logger.info("目前店铺总数: %s, 正在记录店铺信息...,请稍等." % browser_size)
        for index, browser in enumerate(shop_info['browserList']):
            index += 1
            print(browser['browserName'] + "====" + browser['browserOauth'])
        return shop_info['browserList']
    else:
        if "err" not in shop_info:
            shop_info["err"] = ""
        logger.warning("statusCode:%s, err: %s" % (shop_info['statusCode'], shop_info['err']))
        return 0
