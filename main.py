from back_tester import  Backtester
import datetime as dt
import matplotlib.pyplot as plt


"""
交易订单:

"Received order" 表示接收到新的交易订单。
"Filled" 表明订单已经执行，包括具体的买卖操作，数量，价格等信息。
持仓状态:

"Net" 表示净持仓数量，正数代表多头持仓，负数代表空头持仓。
"Value" 是当前持仓的市场价值。
"UPnL" (Unrealized Profit and Loss) 未实现盈亏，指当前持仓的浮动盈亏。
"RPnL" (Realized Profit and Loss) 实现盈亏，指已平仓部分的实际盈亏。
"""


if __name__ == '__main__':
    # 设置回测参数
    symbol = 'AAPL'
    start_date = dt.datetime(2023, 1, 1)
    end_date = dt.datetime(2024, 1, 1)
    #data_source = 'yahoo'

    # 创建并启动回测器
    backtester = Backtester(symbol, start_date, end_date)
    backtester.start_backtest()
    backtester.rpnl.plot()
    backtester.upnl.plot()
    plt.show()