import state_line


class AvgLine(state_line.StateLine):
    # AvgLine 历史平均线
    def __init__(self, origin: list) -> None:
        self.set_origin(origin)

    def op(self):
        origin = sorted(self.origin, key=lambda x: x[0], reverse=False)
        total = 0
        min_val = 999
        max_val = 0
        for item in origin:
            f_item = float(item[1])
            if f_item < min_val:
                min_val = f_item
            if f_item > max_val:
                max_val = f_item
            total += f_item

        avg = total / len(origin)

        m = {
            "avg": [avg, "blue", "平均值", [], []],
            "max": [max_val, "gold", "最大值", [], []],
            "min": [min_val, "cyan", "最小值", [], []],
            "max_2": [(max_val - avg) * 0.2 + avg, "peru", "max_2", [], []],
            "max_4": [(max_val - avg) * 0.4 + avg, "peru", "max_4", [], []],
            "max_6": [(max_val - avg) * 0.6 + avg, "peru", "max_6", [], []],
            "max_8": [(max_val - avg) * 0.8 + avg, "peru", "max_8", [], []],
            "min_2": [(avg - min_val) * 0.2 + min_val, "skyblue", "min_2", [], []],
            "min_4": [(avg - min_val) * 0.4 + min_val, "skyblue", "min_4", [], []],
            "min_6": [(avg - min_val) * 0.6 + min_val, "skyblue", "min_6", [], []],
            "min_8": [(avg - min_val) * 0.8 + min_val, "skyblue", "min_8", [], []],
        }

        for item in origin:
            # 日期
            dt = item[0]
            for ttype in m:
                x_arr = m[ttype][3]
                y_arr = m[ttype][4]
                x_arr.append(dt)
                y_arr.append(m[ttype][0])

        ret = []
        for ttype in m:
            x = m[ttype][3]
            y = m[ttype][4]
            color = m[ttype][1]
            label = m[ttype][2]
            ret.append([x, y, color, label])
        return ret
