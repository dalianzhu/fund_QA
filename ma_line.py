import state_line


class MA(state_line.StateLine):
    # 均值曲线
    def __init__(self, origin: list, avg_date: int, color: str) -> None:
        self.avg_date = avg_date
        self.color = color
        self.set_origin(origin)

    @staticmethod
    def get_sum(origin):
        val = 0
        for item in origin:
            v = float(item[1])
            val += v
        return val / len(origin)

    def op(self):
        origin = sorted(self.origin, key=lambda x: x[0], reverse=False)
        x = []
        y = []
        index = 0
        for item in origin:
            # 日期
            dt = item[0]
            index += 1
            if index < self.avg_date:
                pass
            else:
                v = MA.get_sum(origin[index - self.avg_date:index])
                x.append(dt)
                y.append(v)

        self.ma20_dx = []
        self.ma20_dy = []
        last = y[0]
        for i, item in enumerate(y):
            date = x[i]
            self.ma20_dx.append(date)
            self.ma20_dy.append((item - last) * 10)
            last = item

        self.ma20_ddx = []
        self.ma20_ddy = []
        last = self.ma20_dy[0]
        for i, item in enumerate(self.ma20_dy):
            date = x[i]
            self.ma20_ddx.append(date)
            self.ma20_ddy.append((item - last))
            last = item

        return [
            [x, y, self.color, "MA{}".format(self.avg_date)],
            [self.ma20_dx, self.ma20_dy, self.color, "dMA{}".format(self.avg_date)],
            [self.ma20_ddx, self.ma20_ddy, self.color, "ddMA{}".format(self.avg_date)]
        ]
