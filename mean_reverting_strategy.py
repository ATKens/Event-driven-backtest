"""
基于均值回归的交易策略，继承strategy
"""
import pandas as pd
from strategy import Strategy


class MeanRevertingStrategy(Strategy):
    def __init__(self, symbol, lookback_intervals=20, buy_threshold=-1.5, sell_threshold=1.5):
        """
        初始化均值回归策略实例。
        参数:
        symbol : str                - 被交易的资产标志符，如股票代码。
        lookback_intervals : int   - 用于计算Z-score的回看区间长度。
        buy_threshold : float      - 触发买入信号的Z-score下阈值。
        sell_threshold : float     - 触发卖出信号的Z-score上阈值。
        """
        super().__init__()  # 调用基类的构造函数
        self.symbol = symbol
        self.lookback_intervals = lookback_intervals
        self.buy_threshold = buy_threshold
        self.sell_threshold = sell_threshold
        self.prices = pd.DataFrame()  # 初始化存储价格数据的DataFrame
        self.is_long, self.is_short = False, False  # 初始化持仓状态标志

    def event_position(self, positions):
        """
        处理头寸更新事件。
        参数:
        positions : dict - 包含所有头寸信息的字典。
        """
        if self.symbol in positions:
            position = positions[self.symbol]
            self.is_long = True if position.net > 0 else False
            self.is_short = True if position.net < 0 else False

    def event_tick(self, market_data):
        """
        处理市场数据更新事件。
        参数:
        market_data : MarketData - 包含最新市场数据的对象。
        """

        self.store_prices(market_data)
        if len(self.prices) < self.lookback_intervals:
            return  # 如果数据不足以计算Z-score，则返回
        signal_value = self.calculate_z_score()
        timestamp = market_data.get_timestamp(self.symbol)

        if signal_value < self.buy_threshold:
            self.on_buy_signal(timestamp)
        elif signal_value > self.sell_threshold:
            self.on_sell_signal(timestamp)

    def store_prices(self, market_data):
        """
        存储市场价格数据。
        参数:
        market_data : MarketData - 包含市场价格信息的对象。
        """
        timestamp = market_data.get_timestamp(self.symbol)
        self.prices.loc[timestamp, 'close'] = market_data.get_last_price(self.symbol)
        self.prices.loc[timestamp, 'open'] = market_data.get_open_price(self.symbol)
        #print(self.prices.tail(3))

    def calculate_z_score(self):
        """
        计算并返回最新的Z-score。
        """
        prices = self.prices[-self.lookback_intervals:]
        returns = prices['close'].pct_change().dropna()
        z_score = (returns - returns.mean()) / returns.std()
        return z_score.iloc[-1]

    def on_buy_signal(self, timestamp):
        """
        处理买入信号。
        参数:
        timestamp : datetime - 信号发出的时间戳。
        """
        if not self.is_long:
            self.send_market_order(self.symbol, 100, True, timestamp)

    def on_sell_signal(self, timestamp):
        """
        处理卖出信号。
        参数:
        timestamp : datetime - 信号发出的时间戳。
        """
        if not self.is_short:
            self.send_market_order(self.symbol, 100, False, timestamp)