import my_plot
import matplotlib.pyplot as plt


class Fig(object):
    # 封装figure对象
    def __init__(self, total_plots_len) -> None:
        self.fig = plt.figure()
        self.total_plots_len = total_plots_len
        self.index = 0

    def add_sub_plot(self) -> my_plot.Plot:
        print("total_plots_len {} {}".format(
            self.total_plots_len,  self.index))
        size = 0
        if self.total_plots_len == 1:
            size = 110
        elif 1 < self.total_plots_len <= 4:
            size = 220
        elif 4 < self.total_plots_len <= 6:
            size = 320
        elif 6 < self.total_plots_len <= 9:
            size = 330
        else:
            raise Exception("图太多了")

        self.index += 1
        p = self.fig.add_subplot(size+self.index)

        return my_plot.Plot(p)
