import json

import check_strategy.check_ma20 as check_ma20
import check_strategy.check_fixed as check_fixed


def run_check_ma20(code):
    with open("./db_{}.json".format(code), "rb")as f:
        text = f.read()
        origin = json.loads(text)
        # check_ma20.check_ma20(origin)
        # before sale, before buy
        tp = check_ma20.check_ma20_du(origin, [5, 5])
        print(tp)
    # max_val = 0
    # max_sale_day = 0
    # max_buy_day = 0
    # for i in range(1, 15):
    #     for j in range(1, 15):
    #         tp = check_ma20.check_ma20_du(origin, [i, j])
    #         if tp > max_val:
    #             max_val = tp
    #             max_sale_day = i
    #             max_buy_day = j
    # print("max:{}, before sale:{} before buy:{}".format(max_val, max_sale_day, max_buy_day))


def run_check_fix(code):
    with open("./db_{}.json".format(code), "rb")as f:
        text = f.read()
        origin = json.loads(text)
        # check_ma20.check_ma20(origin)
        # before sale, before buy
        tp = check_fixed.check_ma20_fixed(origin)
        print(tp)


codes = {
    "005918": "天弘沪深300",
    "502000": "西部利得中证500指数增强A",
}

# run_check_fix("005918")
# run_check_fix("502000")

# run_check_ma20("005918")
# run_check_ma20("502000")
run_check_ma20("006341")
# run_check_ma20("003567")
