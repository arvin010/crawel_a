import logging
from time import sleep

logging.basicConfig(filename="train_log", format='%(asctime)s - %(name)s - %(levelname)s -%(module)s:  %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S ',
                    level=logging.INFO)
logger = logging.getLogger()
KZT = logging.StreamHandler()
KZT.setLevel(logging.DEBUG)
logger.addHandler(KZT)





def select_country(self,driver,country=None,date=None):
    country_dict={"MX":"A1AM78C64UM0Y8","CA":"A2EUQ1WTGCTBG2","US":"ATVPDKIKX0DER","BR":"A2Q3Y263D00KWC"}
    # driver.find_element(by=By.XPATH ,value=f'//*[@id="{country_dict[country]}"]').click()  #select country
    driver.find_element(by=By.XPATH ,value='//*[@id="partner-switcher"]/button').click()  #select country
    sleep(0.5)
    driver.find_element(by=By.XPATH ,value=f'//*[@id="{country_dict[country]}"]').click()  #select country
    return driver
