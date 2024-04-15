import requests
from datetime import datetime, timedelta
import json
from pymongo import MongoClient

# MongoDB Configuration
client = MongoClient("localhost", 27017)
db = client["hamburger"]  # 创建名为 hamburger 的数据库


def time_to_date(time):
    # 时间戳转换为日期
    timestamp = time / 1000  # 将毫秒转换为秒
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")


def date_to_time(date):
    # 将日期字符串转换为时间戳（毫秒）
    date_obj = datetime.strptime(date, "%Y-%m-%d")
    timestamp_seconds = date_obj.timestamp()
    return int(timestamp_seconds * 1000)


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
    # 设置获得的金价数据条目数
    pageSize = 10

    # data_style表示返回金价类型:{'基础':'JO_52683','零售':'JO_52684','回收':'JO_52685'}
    data_styles = ["JO_52683", "JO_52684", "JO_52685"]

    # 爬取你需要的总页数
    pageMax = 313

    for count in range(pageMax):
        print(f"Retrieving data for page {count + 1}...")
        # 获取今天的日期
        date_str = (datetime.now() - timedelta(days=count)).strftime("%Y-%m-%d")
        time_milliseconds = date_to_time(date_str)

        for data_style in data_styles:
            quote_json = getPageData(
                pageSize, count, data_style, header, time_milliseconds
            )
            item = quote_json["data"][data_style][-1]  # 获取最后一条数据
            # 查找数据库中是否存在该日期的记录
            existing_record = db.gold.find_one({"date": date_str})
            if existing_record:
                # 如果存在，则更新记录
                update_query = {"$set": {data_style: item["q1"]}}
                db.gold.update_one({"date": date_str}, update_query)
            else:
                # 如果不存在，则插入新记录
                data_dict = {"date": date_str, data_style: item["q1"]}
                db.gold.insert_one(data_dict)
        print(f"Data retrieval for page {count + 1} completed.")

    print("Data retrieval completed.")


if __name__ == "__main__":
    main()
