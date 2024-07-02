from order import Order

"""
Strategy 类框架提供了处理交易策略所需的基本方法结构，使得可以根据不同的交易逻辑定制具体实现。
通过定义具体的事件处理函数，可以实现自动交易策略，如基于某些市场条件自动买入或卖出股票。
"""
class Strategy:
    def __init__(self):
        """
        初始化 Strategy 类的一个实例。
        """
        self.event_sendorder = None  # 用于发送订单的事件处理函数，初始设为 None

    def event_tick(self, market_data):
        """
        处理市场数据更新的事件。
        参数:
        market_data : 包含市场价格更新等信息的数据对象
        """
        pass

    def event_order(self, order):
        """
        处理订单更新事件。
        参数:
        order : 包含订单详细信息的订单对象
        """
        pass

    def event_position(self, positions):
        """
        处理头寸更新事件。
        参数:
        positions : 包含当前所有头寸信息的列表或对象
        """
        pass

    def send_market_order(self, symbol, qty, is_buy, timestamp):
        """
        发送市场订单。
        参数:
        symbol : 交易的标的符号，如股票代码
        qty : 订单的数量
        is_buy : 布尔值，指示是买入还是卖出
        timestamp : 订单的时间戳
        """
        if not self.event_sendorder is None:
            order = Order(timestamp, symbol, qty, is_buy, True)  # 创建订单对象
            self.event_sendorder(order)  # 调用事件处理函数发送订单
