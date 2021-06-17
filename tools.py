import sys
from typing import ForwardRef
import qa
import datetime
import os
import time
import requests
import json
import re
from bs4 import BeautifulSoup
import valuation_line
import ma_line

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


def run(op):
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
    if op == "today":
        run("refresh")
        codes = {
            "005918": "天弘沪深300",
            "502000": "西部利得中证500指数增强A",
        }
        send_msg = []
        for code in codes:
            title = codes[code]
            # 加载原数据
            with open("./db_{}.json".format(code), "rb")as f:
                text = f.read()
                origin = json.loads(text)
                val = valuation_line.Valuation(origin, title)
                ret = val.op()
                valx = ret[0][0]
                valy = ret[0][1]

                ma20 = ma_line.MA(origin, 20, "green")
                ret = ma20.op()
                ma20x = ret[0][0]
                ma20y = ret[0][1]
                if valx[-1] != ma20x[-1]:
                    raise Exception("日期对不上")
                date = valx[-1]
                val_today = float(valy[-1])
                ma20_today = float(ma20y[-1])
                ret = {
                    "title": title,
                    "date": date,
                    "val": val_today,
                    "ma20": ma20_today,
                    "suggestion": ""
                }
                if val_today < ma20_today:
                    ret["suggestion"] = "卖出"
                else:
                    ret["suggestion"] = "持有"
                print(ret)
                send_msg.append(ret)
        send_msg_str = ""
        for msg in send_msg:
            send_msg_str += "名称：{} 当前：{:.4} ma20：{:.4} 建议:{}\n".format(
                msg["title"], msg["val"], msg["ma20"], msg["suggestion"])
        # 发送通知
        # send_msg_feige("", send_msg_str)


def send_msg_feige(id, text):
    body = {
        "msgContent": text,  # 文本消息内容
        "chatId": [
            id,
        ],
        "multiGroupMode": 0,
        "duplicateCheckInterval": 120,
        "duplicateCheckMode": 0
    }
    ret = requests.post(
        "",
        data=json.dumps(body))
    print(ret)


def main():
    op = sys.argv[1]
    run(op)


if __name__ == "__main__":
    main()
