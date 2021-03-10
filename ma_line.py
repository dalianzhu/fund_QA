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
        return val/len(origin)

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
                v = MA.get_sum(origin[index-self.avg_date:index])
                x.append(dt)
                y.append(v)
        return x, y, self.color, "MA{}".format(self.avg_date)
