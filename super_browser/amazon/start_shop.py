import logging
from socket import *
from time import sleep
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from util.com import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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





def start_browser(self, browserOauth="azRUaVhpWlR4cDk0alZPVnovUEl2Zz09"):
    """
    启动店铺
    :param shop_id: 店铺ID
    :return:
    """
    # 启动店铺(两种方式) startBrowser / getBrowserEnvInfo
    start_params = self.browser_api( "startBrowser" ,
                                    {"browserOauth": browserOauth, "isHeadless": self.IS_HEADLESS,
                                        "launcherPage": "https://sellercentral.amazon.co.uk"})
    shop_obj = self.socket_communication(start_params)
    logger.info("启动店铺信息: %s" % shop_obj)
    return shop_obj

def getBrowserEnvInfo(self, browserOauth="azRUaVhpWlR4cDk0alZPVnovUEl2Zz09"):
    """
    启动店铺
    :param shop_id: 店铺ID
    :return:
    """
    # 启动店铺(两种方式) startBrowser / getBrowserEnvInfo
    start_params = self.browser_api(self.__GET_BROWSER_ENV_INFO,
                                    {"browserOauth": browserOauth, "isHeadless": self.IS_HEADLESS,
                                        "launcherPage": "https://sellercentral.amazon.co.uk"})
    shop_obj = self.socket_communication(start_params)
    logger.info("启动店铺信息: %s" % shop_obj)
    return shop_obj



def shop(self,browserOauth=None):
    data = start_browser(self,browserOauth=browserOauth)
    # data = self.getBrowserEnvInfo()
    logger.info(data)
    options = Options()
    debuggerAddress = "127.0.0.1:{}".format(data['debuggingPort'])
    logger.info(debuggerAddress)
    options.add_experimental_option("debuggerAddress", debuggerAddress)
    options.add_argument("--disable-plugins=false")
    options.add_argument("--disable-java=false")
    options.add_argument("--disable-javascript=false")
    options.add_argument("--disable-plugins=false")
    options.add_argument("--no-sandbox=true")
    options.add_argument("--lang=zh-CN")

    s=Service(executable_path=self.config.get("executable_path"))
    driver = webdriver.Chrome( options=options,service=s)
    # driver.implicitly_wait(30)
    driver.get("https://sellercentral.amazon.com")
    try:
        sleep(2)
        driver.find_element(by=By.XPATH,
                            value='//*[@class="text align-end color-white font-size-default ember font-normal"]//a').click()
        sleep(1)
    except:
        pass   #//*[@id="ap-account-switcher-container"]/div[1]/div/div/div[2]/div[1]/div[2]/a/div/div/div/div/div[2]/div/div/div[1]/div[1]
    try:
        driver.find_element(by=By.XPATH,
                            value='//*[@id="ap-account-switcher-container"]/div[1]/div/div/div[2]/div[1]/div[2]/a/div/div/div').click()
        sleep(1)
    except Exception as err:
        pass
    try:
        driver.find_element(by=By.ID, value="signInSubmit").click()
    except:
        try:
            driver.find_element(by=By.XPATH, value='//div[@class="a-column a-span12"][0]').click()
            sleep(1)
            driver.find_element(by=By.ID, value="signInSubmit").click()
        except:
            pass
    try:
        driver.find_element(by=By.XPATH, value='//*[@id="signInSubmit"]').click()
    except :
        pass
    sleep(1)
    # text = driver.find_element(by=By.XPATH,
                            #    value='//div[@class="css-93gqc1"][4]//span[@class="css-kws921 e1i7w3tc50"]').text
    try:
        driver.find_element(by=By.XPATH ,value='//*[@id="picker-container"]/div/div[2]/div/div[3]/div/div[3]/button/div/div').click()
    except Exception as err:
        pass
    try:
        driver.find_element(by=By.XPATH ,value='//*[@id="picker-container"]/div/div[3]/div/button').click()
    except Exception as err:
        pass
    return driver