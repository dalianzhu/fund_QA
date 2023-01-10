import valuation_line
import datetime
import ma_line


class StrategyFixed(object):
    def __init__(self, origin) -> None:
        self.last_buy_date = 0
        self.origin = origin
        val = valuation_line.Valuation(self.origin, "")
        ret = val.op()[0]
        self.valx = ret[0]  # 日期
        self.valy = ret[1]  # 值
        self.date_map_val = {date: index for (index, date) in enumerate(self.valx)}

    def run(self, date: str, period_money, fund_val) -> (str, float):  # sale/buy, 1,0
        if datetime.datetime.strptime(date, "%Y-%m-%d").weekday() == 2:
            return "buy", 1
        if period_money != 0 and fund_val / period_money > 11.50:
            return "sale", 1
        return "skip", 0
