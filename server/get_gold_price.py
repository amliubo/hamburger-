import requests
from bs4 import BeautifulSoup as bs4
from datetime import datetime
import json
import time
from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")  # MongoDB连接地址
mongo_db = client["hamburger"]  # 替换为你的数据库名称


def time_to_date(time):
    # 时间戳转换为日期
    timestamp = (
        time / 1000 + 24 * 60 * 60
    )  # 将毫秒转换为秒,因为是UTC时间需加24小时*60分钟*60秒
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")


def date_to_time(date):
    # 将日期字符串转换为datetime对象

    date_format = "%Y-%m-%d"
    date_obj = datetime.strptime(date, date_format)

    # 获取UTC时间的时间戳（秒）
    timestamp_seconds = date_obj.timestamp()

    # 转换为毫秒
    timestamp_milliseconds = int(timestamp_seconds * 1000)
    return timestamp_milliseconds


def getPageData(pageSize, pagecount, data_style, header, time):
    res = requests.get(
        "https://api.jijinhao.com/quoteCenter/historys.htm?codes="
        + data_style
        + "&style=3&pageSize="
        + str(pageSize)
        + "&currentPage="
        + str(pagecount)
        + "&_="
        + str(time),
        headers=header,
    )
    # 获得json变量,里面记录着金价和记录日期
    quote_json_str = res.content.decode("utf-8")
    # print(quote_json_str)
    quote_json = json.loads(quote_json_str[4:].replace("quote_json = ", ""))
    return quote_json


header = {
    "Host": "api.jijinhao.com",
    "Connection": "keep-alive",
    "sec-ch-ua": '"Not A(Brand";v="99", "Microsoft Edge";v="121", "Chromium";v="121"',
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "sec-ch-ua-platform": '"Windows"',
    "Accept": "*/*",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Dest": "script",
    "Referer": "https://quote.cngold.org/gjs/swhj_zghj.html",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Content-Type": "text/html;charset=UTF-8",
    "Connection": "keep-alive",
}


def main():
    # 以下注释代码可以直接传入今天的日期
    date_str = datetime.now().strftime("%Y-%m-%d")

    # 把当前日期传入转换函数后,获得如"1708656891526"这样的毫秒时间戳
    time_milliseconds = date_to_time(date_str)
    # print(time)

    # 设置获得的金价数据条目数(可以设置1-500,但是因为分页数关系,可能最后的一页会报错,设置值越大爬取越快,如果要完整爬取请使用默认值10)
    pageSize = 10

    # data_style表示返回金价类型:{'基础':'JO_52683','零售':'JO_52684','回收':'JO_52685'}
    data_styles = ["JO_52683", "JO_52684", "JO_52685"]

    count = 0
    # 爬取你需要的总页数
    pageMax = 999

    # 初始化数据字典
    data_dict = {"date": date_str}

    while count <= pageMax:
        for data_style in data_styles:
            quote_json = getPageData(
                pageSize, count, data_style, header, time_milliseconds
            )
            item = quote_json["data"][data_style][-1]  # 获取最后一条数据
            data_dict[data_style] = item["q1"]  # 将数据加入字典
        count += 1

    # 打印数据字典
    print("Data to be inserted:")
    print(data_dict)

    # 插入到数据库中
    mongo_db.gold.insert_one(data_dict)


if __name__ == "__main__":
    main()
