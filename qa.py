from os import linesep
import sys
import my_fig
import matplotlib.pyplot as plt
import matplotlib
import state_line
import avg_line
import valuation_line
import ma_line
import sys

import json
from matplotlib.pyplot import MultipleLocator


def draw_ma(fig, code):
    # code = "000905"
    print("draw_ma:{}".format(code))
    title = fund_codes[code]
    # 加载原数据
    with open("./db_{}.json".format(code), "rb")as f:
        text = f.read()
        origin = json.loads(text)

    # 在fig中添加一个子画板
    plot = fig.add_sub_plot()
    # 在子画板上画净值曲线
    plot.add_line(valuation_line.Valuation(origin, title))
    # 在子画板上画MA20曲线
    plot.add_line(ma_line.MA(origin, 20, "green"))
    # 在子画板上画MA60曲线
    plot.add_line(ma_line.MA(origin, 60, "gold"))
    # 在子画板上画MA120曲线
    plot.add_line(ma_line.MA(origin, 120, "black"))


def draw_avg(fig, code):
    print("draw_ma:{}".format(code))
    title = fund_codes[code]
    # 加载原数据
    with open("./db_{}.json".format(code), "rb")as f:
        text = f.read()
        origin = json.loads(text)

    # 在fig中添加一个子画板
    plot = fig.add_sub_plot()
    # 在子画板上画净值曲线
    plot.add_line(valuation_line.Valuation(origin, title))
    # 在子画板上画历年平均值线
    plot.add_line(avg_line.AvgLine(origin))


fund_codes = {
    "502000": "西部利得中证500指数增强A",
    "000478": "建信中证500",
    "002979": "广发中证全指金融地产联接C",
    "004598": "南方中证银行ETF联接C",
    "100032": "富国中证红利",
    "005918": "天弘沪深300",
}

if __name__ == "__main__":
    qi_type = "ma"
    target = ""
    real_fund_codes = fund_codes
    if len(sys.argv) > 1:
        qi_type = sys.argv[1]

    if len(sys.argv) > 2:
        target = sys.argv[2]
        real_fund_codes = {k: v for k, v in fund_codes.items() if k == target}

    print(real_fund_codes)
    if len(real_fund_codes) == 0:
        raise Exception("没有找到 {}".format(target))
    # 创建一个figure
    fig = my_fig.Fig(len(real_fund_codes))
    for code in real_fund_codes:
        if qi_type == "ma":
            draw_ma(fig, code)
        elif qi_type == "avg":
            draw_avg(fig, code)

    plt.show()
