"""
Order 类可以用于交易系统中，用来创建、跟踪和管理交易订单。
它提供了基本的结构来保存关于一个订单的所有必要信息，以及订单是否已经执行的状态跟踪。
可以在此基础上添加更多的功能，比如订单的撤销处理、修改订单属性或集成到更大的交易策略和订单管理系统中
"""
class Order:
    def __init__(self, timestamp, symbol, qty, is_buy, is_market_order, price=0):
        self.timestamp = timestamp  # 订单的时间戳
        self.symbol = symbol        # 交易的股票代码或其他金融工具的符号
        self.qty = qty              # 订单数量
        self.price = price          # 订单价格，对于市价单可能为0
        self.is_buy = is_buy        # 是买单还是卖单的标志，True为买单，False为卖单
        self.is_market_order = is_market_order  # 是否为市价单
        self.is_filled = False      # 订单是否已经完全成交的标志
        self.filled_price = 0       # 成交价格，初始为0，成交后更新
        self.filled_time = None     # 成交时间，初始为None，成交后更新
        self.filled_qty = 0         # 已成交数量，初始为0，成交后更新
