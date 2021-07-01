import state_line


class Valuation(state_line.StateLine):
    # Valuation 每日净值曲线
    def __init__(self, origin: list, label: str) -> None:
        self.label = label
        self.set_origin(origin)

    def op(self):
        origin = sorted(self.origin, key=lambda x: x[0], reverse=False)
        x = []
        y = []
        y0 = []
        y1 = []
        for item in origin:
            # 日期
            dt = item[0]
            x.append(dt)
            # 单位净值
            val = float(item[1])
            y.append(val)
            y0.append(0.5)
            y1.append(0.25)
        return [
            (x, y, "r", "{}净值".format(self.label)),
            (x, y0, "r", "0"),
            (x, y1, "r", "0"),
        ]
