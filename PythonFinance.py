# Importing Libraries
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import datetime as dt
import yfinance as yf  # Switched to yfinance for more reliable data

class Finance():
    def __init__(self):
        style.use('ggplot')
        # Historic Data Since 1 Jan 2015. You can change it according to your preference (yyyy, mm, dd)
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
        
        # Set up the plot
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Plot the actual adjusted close price
        ax1.plot(self.df['Date'], self.df['Close'], label='Stock Price', color='yellow', linewidth=2)

        # Plot the moving average
        ax1.plot(self.df['Date'], self.df['1 ma'], label='5-Day Moving Average', color='cyan', linewidth=2)

        # Add labels, title, and grid
        ax1.set_xlabel("Date")
        ax1.set_ylabel("Price")
        plt.title(f"Ticker Symbol: {ticker}")

        # Generate buy/sell signals and display them on the graph
        C = self.df['Close'].tolist()
        D = self.df['1 ma'].tolist()
        E = self.df['Date'].tolist()
        buy_sell_signal = []

        for i in range(len(C)):
            if C[i] > D[i]:
                action = 'BUY/HOLD'
                buy_sell_signal.append((E[i], C[i], 'green'))  # BUY/HOLD -> Green
            elif C[i] < D[i]:
                action = 'SELL'
                buy_sell_signal.append((E[i], C[i], 'red'))  # SELL -> Red

        # Add buy/sell signals to the graph
        for date, price, color in buy_sell_signal:
            ax1.scatter(date, price, color=color, marker='o', s=50, label=f"Signal: {color}")

        # Display legend and grid
        ax1.legend()
        ax1.grid(True)
        
        plt.show()

if __name__ == "__main__":
    finance = Finance()
    finance.get_moving_avg("KO")  # Example for Coca-Cola (KO). You can change this to any ticker symbol.
