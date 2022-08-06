from multiprocessing import managers
from super_browser.amazon.report.main import amazon_report

country_list=["US" , "MX", "CA"]  # BR
report_dir={'日期范围报告':1}
platform_dir={1:"amazon",2:"aliexpress"}
date="6_2022";report_type='日期范围报告'
data={
    "date_type":2,  # 1 月份  2 自定义
    "date_end":"2022-8-3",
    "date_start":"2022-8-01",
    "report_type":report_dir[report_type],    # 1 "日期范围报告"1
    "save_dir":r"d:\work",
    "default_dir":r"C:\Users\administered\Desktop\Super Browser\易仓AM02-美国",
    "country":"US",
    "platform":1,   # 1  amazon  2  aliexpress
    "shop":"易仓AM02-美国",
    "save_type":1,
    "is_del_loction":2,  # 不删本地
    "browserOauth":"YTNFa0ppZlRxQ0FXOHlSRjNRdXdsZz09",
}



if __name__ == "__main__":

    amazon_report(data=data)