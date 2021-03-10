import sys
import my_fig
import matplotlib.pyplot as plt
import matplotlib
import state_line
import valuation_line
import ma_line

import json
from matplotlib.pyplot import MultipleLocator


def draw_ma(fig, code):
    # code = "000905"
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


fund_codes = {
    "000478": "建信中证500",
    "002979": "广发中证全指金融地产联接C",
    "004598": "南方中证银行ETF联接C",
    "100032": "富国中证红利",
    "005918": "天弘沪深300",
}

if __name__ == "__main__":
    # 创建一个figure
    fig = my_fig.Fig(len(fund_codes))
    for code in fund_codes:
        draw_ma(fig, code)

    plt.show()
