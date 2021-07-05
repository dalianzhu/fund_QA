import valuation_line
import ma_line


class StrategyMa20(object):
    def __init__(self, origin) -> None:
        self.origin = origin
        val = valuation_line.Valuation(self.origin, "")
        ret = val.op()[0]
        self.valx = ret[0]  # 日期
        self.valy = ret[1]  # 值
        ma20 = ma_line.MA(self.origin, 20, "green")
        ret = ma20.op()[0]
        self.ma20x = ret[0]
        self.ma20y = ret[1]
        self.date_map_val = {date: index for (
            index, date) in enumerate(self.valx)}
        self.date_map_ma20 = {date: index for (
            index, date) in enumerate(self.ma20x)}

    def run(self, date: str):  # sale/buy, 1,0
        if date not in self.date_map_val:
            raise Exception("date:{} is not found in value".format(date))
        if date not in self.date_map_ma20:
            raise Exception("date:{} is not found in ma20".format(date))
        date_val_index = self.date_map_val[date]
        date_ma20_index = self.date_map_ma20[date]

        val_target_day = float(self.valy[date_val_index])
        ma20_target_day = float(self.ma20y[date_ma20_index])
        if val_target_day < ma20_target_day:
            # 卖出
            return "sale", 1
        else:
            # 买入
            return "buy", 1


class StrategyMa20DU(object):
    def __init__(self, origin, before_sale, before_buy) -> None:
        self.last_buy_date = 0
        self.origin = origin
        val = valuation_line.Valuation(self.origin, "")
        ret = val.op()[0]
        self.valx = ret[0]  # 日期
        self.valy = ret[1]  # 值
        self.date_map_val = {date: index for (
            index, date) in enumerate(self.valx)}

        ma20 = ma_line.MA(self.origin, 20, "green")
        ma20.op()
        self.ma20_x = ma20.x
        self.ma20_y = ma20.y

        self.ma20_dx = ma20.ma20_dx
        self.ma20_dy = ma20.ma20_dy
        self.ma20_ddx = ma20.ma20_ddx
        self.ma20_ddy = ma20.ma20_ddy

        self.date_map_ma20 = {v: k for (k, v) in enumerate(self.ma20_dx)}
        ma20dymap = {}
        ma20map = {}
        for i, item in enumerate(self.ma20_dx):
            ma20dymap[item] = self.ma20_dy[i]
            ma20map[item] = self.ma20_y[i]
        print(ma20map)
        print(ma20dymap)
        self.before_sale = before_sale
        self.before_buy = before_buy

    def check_strict(self, slice, index, days, check_type):
        # 如果checktype = -1，则检查所有的值小于0
        before = index - days
        if before < 0:
            return False
        for i in range(before, index):
            if slice[i] * check_type < 0:
                return False
        return True

    def check(self, slice, index, days, check_type):
        # 如果checktype = -1，则检查所有的值小于0
        before = index - days
        if before < 0:
            return False
        match = 0
        un_match = 0
        for i in range(before, index):
            # print(i)
            # if self.ma20_dy[i] * check_type < 0:
            if slice[i] * check_type < 0:
                un_match += 1
            else:
                match += 1
        return match / (match + un_match) > 0.7

    def run(self, date: str):  # sale/buy, 1,0
        if date not in self.date_map_ma20:
            raise Exception("date:{} is not found in ma20".format(date))
        date_ma20_index = self.date_map_ma20[date]
        date_val_index = self.date_map_val[date]
        val_target_day = self.valy[date_val_index]
        dma20_target_day = float(self.ma20_dy[date_ma20_index])
        ma20_target_day = float(self.ma20_y[date_ma20_index])

        if self.check_strict(self.ma20_dy, date_ma20_index, 3, -1):
            return "sale", 1
        if self.check(self.ma20_dy, date_ma20_index, 10, +1) and \
                self.check_strict(self.ma20_ddy, date_ma20_index, 3, +1):
            self.last_buy_date = date_ma20_index
            return "buy", 1
        return "skip", 0
