from matplotlib.pyplot import MultipleLocator
import matplotlib


class Plot(object):
    # 封装plot对象

    # 传入plot对象
    def __init__(self, plot) -> None:
        self.plot = plot

    def add_line(self, line):
        # ax = plt.gca()
        # ax.xaxis.set_major_locator(x_major_locator)
        # plt.legend()
        line.draw(self.plot)

        x_major_locator = MultipleLocator(30)
        self.plot.xaxis.set_major_locator(x_major_locator)
        matplotlib.rcParams['font.family'] = 'SimSun'
        self.plot.legend()  # 显示图例
        return self
