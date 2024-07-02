"""存储单个数据单元"""
class TickData:
    """Store a single unit of data"""

    def __init__(self, symbol, timestamp, last_price=0, total_volume=0):
        self.symbol = symbol  # 交易标的符号，例如股票代码
        self.timestamp = timestamp  # 时间戳，记录这个数据点的具体时间
        self.last_price = last_price  # 最后成交价格，默认为0
        self.total_volume = total_volume  # 总成交量，默认为0
        self.open_price = 0  # 开盘价，这里默认初始化为0
