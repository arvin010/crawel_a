import logging
from time import sleep,time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from util.com import *

from pykeyboard import PyKeyboard
from pymouse import *
m = PyMouse()
kb=PyKeyboard()


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


def get_report(driver,data):
    """
    driver.find_element(by=By.XPATH ,value='//*[@id="KpiCardList"]/div/div[1]/div/div[4]/casino-knowhere-layer/div/button/div/div/div[2]').click()
    e_list=driver.find_elements(by=By.XPATH,value='//*[@id="KpiCardList"]/div/div[1]/div/div[4]/casino-knowhere-layer/div/div/div/div[3]/div/div[2]/div')
    print(e_list)
    for el in e_list:
        print("店铺总余额:" + el.find_element_by_css_selector('a.title').text)
        print(">"*10)
    """
    # driver.switch_to.frame(driver.find_element_by_id('sc-navtab-reports-t2'))
    # select_elm = Select(driver.find_element_by_class_name('sc-menu-trigger sc-tab-a'))
    print(11111111111111111111111111)
    sleep(0.5)
    driver.find_element(by=By.XPATH ,value='//*[@id="sc-navtab-reports-t2"]/a').click()  #//*[@id="sc-navtab-reports-t2"]/a  //*[@id="sc-navtab-reports-t2"]/a
    # select_ele = Select(ele)
    # select_ele.select_by_index(1).click()
    sleep(0.5)
    driver.find_element(by=By.XPATH ,value='//*[@id="sc-navtab-reports-t2"]/ul/li[2]/a').click()  #//*[@id="sc-navtab-reports-t2"]/ul/li[2]/a  

    # gen reports
    sleep(0.5)
    if data['report_type']==1:
                                                
        # driver.find_element(by=By.CSS_SELECTOR("kat-tab[tab-id='DATE_RANGE_REPORTS']")).click()  # 日期范围报告
        try:
            driver.find_element(by=By.XPATH ,value='//*[@id="root"]/div/div[1]/article/section[2]/div/kat-tabs/kat-tab[6]/span').click()  # 日期范围报告
        except:
            pass
        try:
            driver.find_element(by=By.XPATH ,value='//*[@id="root"]/div/div[1]/article/section[2]/div/kat-tabs/kat-tab[5]/span').click()
        except:
            pass
    
    driver.find_element(by=By.XPATH ,value='//*[@id="drrGenerateReportButton"]/span').click()
    try:
        driver.find_element(by=By.XPATH ,value='//*[@id="drrReportTypeRadioTransaction"]').click()  #//*[@id="drrReportTypeRadioTransaction"]
    except :
        pass
    if data["date_type"]==1: # 月份
        ele=driver.find_element(by=By.ID ,value='drrMonthlySelect')  #//*[@id="drrMonthlySelect"]
        sleep(0.5)
        select_ele = Select(ele)
        sleep(0.5)
        select_ele.select_by_value(data["data_end"])
    elif data["date_type"]==2: # 自定义
        driver.find_element(by=By.XPATH ,value='//*[@id="drrReportRangeTypeRadioCustom"]').click()  # 自定义
        input_start=driver.find_element(by=By.ID ,value='drrFromDate')
        input_start.send_keys("/".join(data["date_start"].split("-")[::-1]))
        input_start.click()
        sleep(0.5)
        # driver.find_element(by=By.XPATH ,value=f'//*[@id="a-popover-content-3"]/div/div/table/tbody/tr[{get_week(data["date_start"])["week_num"]}]/td[{get_week(data["date_start"])["week_day"]}]/a').click()
        input_end=driver.find_element(by=By.XPATH ,value='//*[@id="drrToDate"]')
        input_end.send_keys("/".join(data["date_end"].split("-")[::-1]))
        input_end.click()
        # sleep(3)
        # driver.find_element(by=By.XPATH ,value=f'//*[@id="a-popover-content-3"]/div/div/table/tbody/tr[{get_week(data["date_end"])["week_num"]}]/td[{get_week(data["date_end"])["week_day"]}]/a').click()
    sleep(0.5)
    driver.find_element(by=By.XPATH, value='//*[@id="drrGenerateReportsGenerateButton"]/span/input').click()
    driver.refresh()
    flush=True
    while flush:
        try:
            sleep(10)
            driver.find_element(by=By.XPATH, value='//*[@id="0-ddrAction"]/div/a').click()
        except Exception as err:
            flush =False 
    dtime=driver.find_element(by=By.XPATH, value='//*[@id="0-ddrRequestDate"]/div/span').text
    # if f"{today.year}年{today.month}月{int(today.day)-1}日" == dtime:
    driver.find_element(by=By.XPATH, value='/html/body/div[1]/div[2]/div[7]/div/div/div/div[5]/div/table/tbody/tr[2]/td[4]/span/span').click()
    # m.move(500,600)
    # m.move(1000,800)
    # # print(66666666666666666,m.position())
    m.click(500, 550, button=1, n=1)
    sleep(1)
    # pyperclip.copy(dtime)
    
    # kb.press_key(kb.control_key)
    # kb.tap_key('V')
    
    # kb.release_key(kb.control_key)
    file_name=f'{data["date_start"]}_{data["date_end"]}_{time()}_MonthlyTransaction_{data["country"]}.csv'
    kb.type_string(file_name)
    m.click(500, 500, button=1, n=1)
    # sleep(1)
    # kb.press_key(kb.left_key)
    sleep(0.5)
    kb.press_key(kb.enter_key)
    sleep(10)
    return file_name
