import pandas_datareader.data as web
from market_data import MarketData
import yfinance as yf


class MarketDataSource:
    """
    从外部数据源下载价格信息的类。
    """

    def __init__(self):
        """
        初始化 MarketDataSource 实例。
        """
        self.event_tick = None  # 用于事件驱动逻辑的可调用对象（如果有的话）
        self.ticker, self.source = None, None  # 股票代码和数据来源
        self.start, self.end = None, None  # 查询数据的开始和结束日期
        self.md = MarketData()  # 创建 MarketData 实例以存储和管理市场数据

    def start_market_simulation(self):
        """
        启动市场数据模拟，下载数据并填充到 MarketData 实例中。
        """
        try:
            #data = web.DataReader(self.ticker, self.source, self.start, self.end)

            data = yf.download(self.ticker, start=self.start, end=self.end)

            if data.empty:
                print("No data to process.")  # 检查数据是否为空
                return
            else:
                # 保存到 CSV 文件
                file_name = "data.csv"
                data.to_csv(file_name)
                print(f"Data saved to {file_name}")

        except Exception as e:
            print(f"Failed to fetch data for {self.ticker}: {e}")
            return

        # 遍历下载的数据，并更新到 MarketData 实例
        for time, row in data.iterrows():
            # 添加最新成交价和成交量
            self.md.add_last_price(time, self.ticker, row["Close"], row["Volume"])
            # 添加开盘价
            self.md.add_open_price(time, self.ticker, row["Open"])

            # 如果定义了事件触发函数并且事件触发函数不为空，则调用事件触发函数
            if self.event_tick is not None:
                self.event_tick(self.md)
        print('self.md初始化完成...')


