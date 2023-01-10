import strategy.strategy_fixed as strategy_fixed


def check_ma20_fixed(origin):
    strategy = strategy_fixed.StrategyFixed(origin)
    date_arr = [x[0] for x in origin]
    date_arr.sort()

    per_money = 1000
    total_earn_money = 0
    total_cost_money = 0
    current_num_of_fund = 0

    # 在上次卖出和现在共投入的钱
    period_money = 0

    val_today = 0
    for date in date_arr:
        try:
            op, percent = strategy.run(date, period_money, current_num_of_fund * val_today)
        except Exception as err:
            print(err)
            continue
        val_today = strategy.valy[strategy.date_map_val[date]]

        if op == "skip":
            continue
        elif op == "sale":
            can_sale_fund = current_num_of_fund * percent
            can_earn_money = can_sale_fund * val_today
            if can_sale_fund == 0:
                continue
            current_num_of_fund -= can_sale_fund  # 等于0
            period_money = 0

            total_earn_money += can_earn_money
            print("date:{} sale:{},total cost:{} fund:{},period:{} earn:{}".format(
                date, can_sale_fund, total_cost_money, current_num_of_fund, period_money, total_earn_money))
        elif op == "buy":
            # 定投
            can_buy_money = per_money * percent
            if can_buy_money == 0:
                continue
            fund_share = can_buy_money / val_today
            # 把钱减去，用来买基金
            current_num_of_fund += fund_share
            total_cost_money += can_buy_money
            period_money += can_buy_money
            print("date:{} buy:{}, cost money:{}, fund:{} period:{}".format(
                date, can_buy_money, total_cost_money, current_num_of_fund, period_money))

    # print("current_money:{}, current_fund:{} total_money:{}".format(current_money, current_num_of_fund,
    #                                                                 current_money + current_num_of_fund * val_today))
    return current_num_of_fund * val_today + total_earn_money
