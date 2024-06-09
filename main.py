import sys
import yfinance as yf
import warnings
warnings.filterwarnings("ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated")
from PyQt5.QtWidgets import QApplication
from plotting import calc_and_chart
from app import StockPlotterApp


def main():
    # # example usage
    # stock_to_use = 'AAPL'
    # df = yf.download(tickers=stock_to_use, start='2010-10-10', end='2014-10-10', interval='1d')
    print("Enter the stock symbol to chart (e.g. 'AAPL' for Apple).")
    stock_to_use = input('Stock to chart: ').upper()
    print("\nEnter the data interval (e.g. '1d' for daily, '1wk' for weekly, '1mo' for monthly).")
    data_interval = input('Data interval: ')
    print("\nEnter the data period (e.g. '1y' for one year, '5d' for five days) or '/' to specify start and end dates.")
    data_period = input('Data period: ')
    if data_period == '/':
        print("\nEnter the start date (YYYY-MM-DD).")
        data_start = input('Data start: ')
        print("\nEnter the end date (YYYY-MM-DD).")
        data_end = input('Data end: ')
        df = yf.download(tickers=stock_to_use, start=data_start, end=data_end, interval=data_interval)
    else:
        df = yf.download(tickers=stock_to_use, period=data_period, interval=data_interval)

    print('Plotting...\n')
    fig = calc_and_chart(stock_to_use, df)
    app = QApplication(sys.argv)
    _ = StockPlotterApp(fig)   
    sys.exit(app.exec_())

        
if __name__ == '__main__':
    main()
