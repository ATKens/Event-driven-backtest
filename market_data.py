from tick_data import TickData

class MarketData:
    """
    MarketData 类的主要功能是作为一个金融市场数据的集中存储和管理系统，
    它可以存储、更新和检索与交易标的相关的市场数据。类的设计使其能够捕捉和存储关键的交易数据，
    如最新成交价格、开盘价格以及相关的时间戳。
    """
    def __init__(self):
        self.__recent_ticks__ = dict()  # 初始化一个私有字典来存储每个交易标的的最新行情数据

    # 添加最新市场价格
    def add_last_price(self, time, symbol, price, volume):
        tick_data = TickData(symbol, time, price, volume)  # 创建一个新的TickData实例
        self.__recent_ticks__[symbol] = tick_data  # 更新该交易标的的最新行情数据

    # 添加开盘价格
    def add_open_price(self, time, symbol, price):
        tick_data = self.get_existing_tick_data(symbol, time)  # 获取或创建TickData实例
        tick_data.open_price = price  # 设置开盘价格

    def get_existing_tick_data(self, symbol, time):
        if not symbol in self.__recent_ticks__:
            tick_data = TickData(symbol, time)  # 如果没有现有数据，创建一个新的TickData实例
            self.__recent_ticks__[symbol] = tick_data  # 存储这个新的TickData实例
        return self.__recent_ticks__[symbol]  # 返回这个交易标的的行情数据

    def get_last_price(self, symbol):
        return self.__recent_ticks__[symbol].last_price  # 从字典中获取指定标的的最后成交价格

    def get_open_price(self, symbol):
        return self.__recent_ticks__[symbol].open_price  # 从字典中获取指定标的的开盘价格

    def get_timestamp(self, symbol):
        return self.__recent_ticks__[symbol].timestamp  # 从字典中获取指定标的的时间戳

