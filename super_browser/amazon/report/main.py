import logging
from this import d
from util.com import *
from util.super_browser import SuperBrowser
from super_browser.amazon.start_shop import *
from super_browser.shoplist.main import *
from super_browser.amazon.report.get_report import get_report
from super_browser.amazon.report.file import move_file
from super_browser.amazon.report.db import report_insert_mysql
import traceback

logging.basicConfig(filename="train_log", format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S ',
                    level=logging.INFO)
logger = logging.getLogger()
KZT = logging.StreamHandler()
KZT.setLevel(logging.DEBUG)
logger.addHandler(KZT)





def amazon_report(data):
    brow = SuperBrowser()
    browserList=browser_list(brow)
    sp=shop(brow,browserOauth=data["browserOauth"])
    try:
        file_name=get_report(sp,data=data)
    except :
        file_name=""
        logger.error(traceback.format_exc())
    if file_name and data["save_dir"]:
        move_file(data=data,file_name=file_name)
    
    report_insert_mysql(data=data)

    # for c in country_list:
    #     data["country"]=c;
    #     driver=superBrowser.crawler(browserOauth=data["browserOauth"])
    #     driver=superBrowser.select_country(driver,country=data["country"])  # US  MX BR CA
    #     superBrowser.get_report(driver,data=data)



    # if browserList :
    #     for browserOauth in browserList :
    #         try:
    #             superBrowser.greg(browserOauth=browserOauth["browserOauth"])
    #         except Exception as err:
    #             logger.warning(err)
    # superBrowser.driver_browser()




if __name__ == "__main__":

    amazon_report()