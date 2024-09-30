# Importing Libraries
import pandas as pd
import datetime as dt
import yfinance as yf  # Switched to yfinance for more reliable data

class Finance():
    def __init__(self):
        # Historic Data Since 1 Jan 2015
        self.start = dt.datetime(2015, 1, 1)
        self.end = dt.datetime.now()

    def get_stock_price(self, ticker):
        try:
            # Fetch data using yfinance
            stock = yf.Ticker(ticker)
            self.df = stock.history(start=self.start.strftime('%Y-%m-%d'), end=self.end.strftime('%Y-%m-%d'))
            self.df.reset_index(inplace=True)
            return self.df
        except Exception as e:
            print(f"Error fetching stock data for {ticker}: {e}")
            return None

    def get_moving_avg(self, ticker):
        # Get stock data
        self.df = self.get_stock_price(ticker)
        
        if self.df is None or self.df.empty:
            print(f"No data available for {ticker}.")
            return

        # Calculate the 5-day moving average
        self.df['1 ma'] = self.df['Close'].rolling(window=5, min_periods=0).mean()
        
        # Print Stock Prices and Moving Averages
        print(f"\nStock Prices and 5-Day Moving Average for {ticker}:\n")
        print(self.df[['Date', 'Close', '1 ma']].tail(10))  # Print the last 10 rows

        # Generate buy/sell signals
        C = self.df['Close'].tolist()
        D = self.df['1 ma'].tolist()
        E = self.df['Date'].tolist()

        print("\nBuy/Sell Signals (Last 10 days):")
        for i in range(len(C)):
            signal = ''
            if C[i] > D[i]:
                signal = 'BUY/HOLD'  # Green signal
            elif C[i] < D[i]:
                signal = 'SELL'  # Red signal
            print(f"Date: {E[i].strftime('%Y-%m-%d')} | Price: {C[i]:.2f} | 5-Day MA: {D[i]:.2f} | Signal: {signal}")

if __name__ == "__main__":
    finance = Finance()
    finance.get_moving_avg("KO")  # Example for Coca-Cola (KO). You can change this to any ticker symbol.
