import pandas as pd
from mean_reverting_strategy import MeanRevertingStrategy
from market_data_source import MarketDataSource
from position import Position

class Backtester:
    def __init__(self, symbol, start_date, end_date, data_source="google"):
        """
        初始化回测器。
        参数:
        symbol : str      - 要回测的股票代码或交易标的符号。
        start_date : str  - 回测的开始日期。
        end_date : str    - 回测的结束日期。
        data_source : str - 数据来源，默认为"google"。
        """
        self.target_symbol = symbol
        self.data_source = data_source
        self.start_dt = start_date
        self.end_dt = end_date
        self.strategy = None
        self.unfilled_orders = []
        self.positions = dict()
        self.current_prices = None
        self.rpnl, self.upnl = pd.DataFrame(), pd.DataFrame()

    def get_timestamp(self):
        """
        获取当前市场价格的时间戳。
        返回:
        datetime - 当前价格的时间戳。
        """
        return self.current_prices.get_timestamp(self.target_symbol)

    def get_trade_date(self):
        """
        获取交易日期，转换时间戳为 '年-月-日' 格式。
        返回:
        str - 格式化后的日期字符串。
        """
        timestamp = self.get_timestamp()
        return timestamp.strftime("%Y-%m-%d")

    def update_filled_position(self, symbol, qty, is_buy, price, timestamp):
        """
        更新持仓状态并记录成交。
        参数:
        symbol : str      - 交易的标的符号。
        qty : int         - 成交数量。
        is_buy : bool     - 是否为买入订单。
        price : float     - 成交价格。
        timestamp : datetime - 成交时间。
        """
        # 获取或创建对应标的的持仓对象
        position = self.get_position(symbol)
        # 记录交易事件，更新持仓
        position.event_fill(timestamp, is_buy, qty, price)
        # 触发策略的持仓更新事件
        self.strategy.event_position(self.positions)
        # 更新实现盈亏（Realized PnL）
        self.rpnl.loc[timestamp, "rpnl"] = position.realized_pnl
        # 打印交易详情
        print(self.get_trade_date(), "Filled:",\
              "BUY" if is_buy else "SELL", qty, symbol, "at", price)

    def get_position(self, symbol):
        """
        获取或创建交易标的的持仓状态。
        参数:
        symbol : str - 交易标的符号。
        返回:
        Position - 持仓状态。
        """
        if symbol not in self.positions:
            position = Position()
            position.symbol = symbol
            self.positions[symbol] = position
        return self.positions[symbol]

    def eventhandler_order(self, order):
        """
        处理订单事件，将未完成的订单存储起来。
        参数:
        order : Order - 订单对象。
        """
        self.unfilled_orders.append(order)
        print(self.get_trade_date(), "Received order:",\
              "BUY" if order.is_buy else "SELL", order.qty, order.symbol)

    def match_order_book(self, prices):
        """
        匹配未完成的订单。
        参数:
        prices : dict - 包含最新价格的字典。
        """
        if len(self.unfilled_orders) > 0:
            self.unfilled_orders = \
                [order for order in self.unfilled_orders
                if self.is_order_unmatched(order, prices)]#这里原先是没有not的

    def is_order_unmatched(self, order, prices):
        """
        检查订单是否可以被匹配并执行。
        参数:
        order : Order - 订单对象。
        prices : dict - 最新价格信息。
        返回:
        bool - 如果订单被匹配则返回 True。
        """
        symbol = order.symbol
        timestamp = prices.get_timestamp(symbol)
        if order.is_market_order and timestamp > order.timestamp:
            order.is_filled = True
            open_price = prices.get_open_price(symbol)
            order.filled_timestamp = timestamp
            order.filled_price = open_price
            self.update_filled_position(symbol, order.qty, order.is_buy,open_price, timestamp)
            self.strategy.event_order(order)
            return False
        return True

    def print_position_status(self, symbol, prices):
        """
        打印指定交易标的的持仓状态。
        参数:
        symbol : str - 交易标的的符号。
        prices : dict - 包含价格信息的字典。
        """
        if symbol in self.positions:
            # 获取对应标的的持仓对象
            position = self.positions[symbol]
            # 从价格信息中获取最新的收盘价
            close_price = prices.get_last_price(symbol)
            # 更新持仓对象中的未实现盈亏（Unrealized PnL）
            position.update_unrealized_pnl(close_price)
            # 在持仓对象的DataFrame中更新未实现盈亏信息
            self.upnl.loc[self.get_timestamp(), "upnl"] = position.unrealized_pnl

            # 打印交易日期及持仓详情
            print(self.get_trade_date(),
                  "Net:", position.net,  # 净持仓数量
                  "Value:", position.position_value,  # 持仓的市场价值
                  "UPnL:", position.unrealized_pnl,  # 未实现盈亏
                  "RPnL:", position.realized_pnl)  # 实现盈亏

    def eventhandler_tick(self, prices):
        """
        处理市场价格更新事件。
        参数:
        prices : dict - 包含最新市场价格的字典。
        """
        # 更新当前价格数据
        self.current_prices = prices
        # 处理市场数据更新事件
        self.strategy.event_tick(prices)
        # 匹配订单簿中的未完成订单
        self.match_order_book(prices)
        # 打印当前持仓状态
        self.print_position_status(self.target_symbol, prices)

    def start_backtest(self):
        """
        初始化并启动回测过程。
        """
        # 为回测器分配选定的策略。
        self.strategy = MeanRevertingStrategy(self.target_symbol)
        # 将策略的订单发送事件链接到回测器的订单处理函数。
        self.strategy.event_sendorder = self.eventhandler_order

        # 创建市场数据源实例。
        mds = MarketDataSource()
        # 将市场数据更新事件链接到回测器的行情处理函数。
        mds.event_tick = self.eventhandler_tick #价格变动事件，当价格发生变动的时候就会调用
        # 为市场数据设置交易标的符号和数据源。
        mds.ticker = self.target_symbol
        mds.source = self.data_source
        # 设置市场数据模拟的开始和结束日期。
        mds.start, mds.end = self.start_dt, self.end_dt

        # 开始回测过程并打印进度消息。
        print("\n------------------------回测开始------------------------")
        mds.start_market_simulation()
        print("\n------------------------回测完成------------------------")

