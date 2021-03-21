import sys
import qa
import datetime
import os
import time
import requests
import json
import re
from bs4 import BeautifulSoup

api = "https://fundf10.eastmoney.com/F10DataApi.aspx?type=lsjz&code={}&page={}&sdate={}&edate={}&per=100"


def get_page(code: str, start_date: str, end_date: str, page: int):
    ret = requests.get(api.format(code, page, start_date, end_date))
    soup = BeautifulSoup(ret.text, 'html.parser')
    heads = []
    pages = 0
    if page == 1:
        for head in soup.findAll("th"):
            heads.append(head.contents[0])
        pattern = re.compile('pages:(.*),')
        result = re.search(pattern, ret.text).group(1)
        pages = int(result)

    records = []
    for row in soup.findAll("tbody")[0].findAll("tr"):
        row_records = []
        for record in row.findAll('td'):
            val = record.contents
            if val == []:
                row_records.append("nil")
            else:
                row_records.append(val[0])
        records.append(row_records)
    return heads, pages, records


def spider(code: str, start_date: str, end_date: str, write_file: bool):
    head, pages, records = get_page(code, start_date, end_date, 1)
    page_records = []
    for item in records:
        page_records.append(item)
    print("head:{}\npages:{}".format(head, pages))

    for i in range(2, pages+1):
        _, _, records = get_page(code, start_date, end_date, i)
        for item in records:
            page_records.append(item)
        time.sleep(0.25)
    js_str = json.dumps(page_records, ensure_ascii=False)
    if write_file:
        with open("./db_{}.json".format(code), "wb+") as f:
            f.write(js_str.encode())
    return page_records


# ['净值日期', '单位净值', '累计净值', '日增长率', '申购状态', '赎回状态', '分红送配']
start_date = "2016-03-05"


def main():
    op = sys.argv[1]
    if op == "refresh":
        for code in qa.fund_codes:
            file_path = "./db_{}.json".format(code)

            end_time = datetime.datetime.now()
            end_time = end_time.strftime("%Y-%m-%d")

            if os.path.exists(file_path) == False:
                spider(code, start_date, end_time, True)
                continue

            with open(file_path, "rb") as f:
                old_data = json.loads(f.read().decode())
            if len(old_data) <= 0:
                return

            latest = old_data[0]
            latest_data = latest[0]
            t_latest = datetime.datetime.strptime(latest_data, "%Y-%m-%d")

            start_time = t_latest + datetime.timedelta(days=1)
            start_time = start_time.strftime("%Y-%m-%d")

            ret = spider(code, start_time, end_time, False)
            all_records = []
            for item in ret:
                if len(item) > 1:
                    all_records.append(item)
            for item in old_data:
                if len(item) > 1:
                    all_records.append(item)

            js_str = json.dumps(all_records, ensure_ascii=False)
            with open("./db_{}.json".format(code), "wb+") as f:
                f.write(js_str.encode())


if __name__ == "__main__":
    main()
