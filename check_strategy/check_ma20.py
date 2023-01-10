import strategy.strategy_ma20 as strategy_ma20


def check_ma20(origin):
    strategy = strategy_ma20.StrategyMa20(origin)
    date_arr = [x[0] for x in origin]
    date_arr.sort()

    current_money = 1000
    current_num_of_fund = 0

    val_today = 0
    for date in date_arr:
        try:
            op, percent = strategy.run(date)
        except:
            continue
        val_today = strategy.valy[strategy.date_map_val[date]]
        ma20_today = strategy.ma20y[strategy.date_map_ma20[date]]
        if op == "buy":
            can_buy_money = current_money * percent
            if can_buy_money == 0:
                continue
            fund_share = can_buy_money / val_today
            # 把钱减去，用来买基金
            current_money -= can_buy_money
            current_num_of_fund += fund_share
            print("date:{} buy:{}, money:{}, fund:{}, val:{}, ma20:{}".format(
                date, can_buy_money, current_money, current_num_of_fund, val_today, ma20_today))
        elif op == "sale":
            can_sale_fund = current_num_of_fund * percent
            can_earn_money = can_sale_fund * val_today
            if can_sale_fund == 0:
                continue
            current_num_of_fund -= can_sale_fund
            current_money += can_earn_money
            print("date:{} sale:{}, money:{}, fund:{}, val:{}, ma20:{}".format(
                date, can_sale_fund, current_money, current_num_of_fund, val_today, ma20_today))

    print("current_money:{}, current_fund:{} total_money:{}".format(current_money, current_num_of_fund,
                                                                    current_money + current_num_of_fund * val_today))


def check_ma20_du(origin, args):
    strategy = strategy_ma20.StrategyMa20DU(origin, args[0], args[1])
    # ret= strategy.check(strategy.date_map_ma20["2018-09-18"], 30, -1)
    # print(ret)
    # return
    date_arr = [x[0] for x in origin]
    date_arr.sort()

    current_money = 1000
    current_num_of_fund = 0

    val_today = 0
    for date in date_arr:
        try:
            op, percent = strategy.run(date)
        except Exception as err:
            # print(err)
            continue
        val_today = strategy.valy[strategy.date_map_val[date]]
        # strategy.check(strategy.ma20_dy, strategy.date_map_val[date], 4, 1)
        # return

        if op == "skip":
            # print("date:{} skip money:{}, fund:{}".format(
            #     date, current_money, current_num_of_fund))
            continue
        elif op == "buy":
            can_buy_money = current_money * percent
            if can_buy_money == 0:
                continue
            fund_share = can_buy_money / val_today
            # 把钱减去，用来买基金
            current_money -= can_buy_money
            current_num_of_fund += fund_share
            print("date:{} buy:{}, money:{}, fund:{}".format(
                date, can_buy_money, current_money, current_num_of_fund))
        elif op == "sale":
            can_sale_fund = current_num_of_fund * percent
            can_earn_money = can_sale_fund * val_today
            if can_sale_fund == 0:
                continue
            current_num_of_fund -= can_sale_fund
            current_money += can_earn_money
            print("date:{} sale:{}, money:{}, fund:{}".format(
                date, can_sale_fund, current_money, current_num_of_fund))

    # print("current_money:{}, current_fund:{} total_money:{}".format(current_money, current_num_of_fund,
    #                                                                 current_money + current_num_of_fund * val_today))
    return current_money + current_num_of_fund * val_today
