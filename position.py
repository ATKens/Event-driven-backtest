"""
 Position 类用于追踪一个交易头寸的各种指标，
如总买入量、总卖出量、净头寸、以及实现和未实现的盈亏等
"""
class Position:
    def __init__(self):
        """
        初始化 Position 类的一个实例。
        """
        self.symbol = None            # 交易的资产标识符，如股票代码
        self.buys = 0                 # 累计购买的数量
        self.sells = 0                # 累计卖出的数量
        self.net = 0                  # 净头寸数量，计算为 buys - sells
        self.realized_pnl = 0         # 实现的盈亏（已平仓部分的盈亏）
        self.unrealized_pnl = 0       # 未实现的盈亏（仍持有部分的盈亏）
        self.position_value = 0       # 头寸的当前市场价值

    def event_fill(self, timestamp, is_buy, qty, price):
        """
        处理交易填充事件，更新头寸状态。

        参数:
        timestamp : datetime       # 事件发生的时间戳
        is_buy : bool              # 是否是买入事件
        qty : int                  # 交易数量
        price : float              # 交易价格
        """
        if is_buy:
            self.buys += qty  # 如果是买入事件，增加累计购买数量
        else:
            self.sells += qty  # 如果是卖出事件，增加累计卖出数量

        self.net = self.buys - self.sells  # 更新净头寸数量
        changed_value = qty * price * (1 if is_buy else -1)  # 计算此次交易的价值变动,这里原先是\
        # (-1 if is_buy else 1)
        self.position_value += changed_value  # 更新头寸的市场价值

        if self.net == 0:
            self.realized_pnl = self.position_value  # 如果净头寸为零，认为所有头寸已平仓，实现的盈亏等于当前头寸价值

    def update_unrealized_pnl(self, price):
        """
        更新未实现盈亏。

        参数:
        price : float             # 最新的市场价格
        """
        if self.net == 0:
            self.unrealized_pnl = 0  # 如果净头寸为零，未实现盈亏为零
        else:
            self.unrealized_pnl = price * self.net + self.position_value  # 计算未实现盈亏
        return self.unrealized_pnl  # 返回计算后的未实现盈亏
