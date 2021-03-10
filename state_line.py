

class StateLine(object):
    # StateLine 抽象函数，表示一个线条
    # 子线条实现op函数，返回 x,y,颜色,label
    def set_origin(self, origin):
        self.origin = origin

    def op(self):
        pass

    def draw(self, plot):
        x, y, color, label = self.op()
        plot.plot(x, y, color=color, label=label)
