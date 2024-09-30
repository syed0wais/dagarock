# Importing Libraries
import pandas as pd
import datetime as dt
import yfinance as yf  # Switched to yfinance for more reliable data
import plotly.graph_objects as go

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
        
        # Create the figure for plotting
        fig = go.Figure()

        # Add stock price line
        fig.add_trace(go.Scatter(x=self.df['Date'], y=self.df['Close'], mode='lines', name='Stock Price', line=dict(color='yellow')))

        # Add 5-day moving average line
        fig.add_trace(go.Scatter(x=self.df['Date'], y=self.df['1 ma'], mode='lines', name='5-Day Moving Avg', line=dict(color='cyan')))

        # Generate buy/sell signals and display them on the graph
        C = self.df['Close'].tolist()
        D = self.df['1 ma'].tolist()
        E = self.df['Date'].tolist()
        buy_signals = []
        sell_signals = []

        for i in range(len(C)):
            if C[i] > D[i]:
                buy_signals.append((E[i], C[i]))  # BUY/HOLD
            elif C[i] < D[i]:
                sell_signals.append((E[i], C[i]))  # SELL

        # Add buy signals to the plot (green markers)
        fig.add_trace(go.Scatter(x=[x[0] for x in buy_signals], y=[x[1] for x in buy_signals],
                                 mode='markers', name='Buy Signal', marker=dict(color='green', size=10)))

        # Add sell signals to the plot (red markers)
        fig.add_trace(go.Scatter(x=[x[0] for x in sell_signals], y=[x[1] for x in sell_signals],
                                 mode='markers', name='Sell Signal', marker=dict(color='red', size=10)))

        # Update layout
        fig.update_layout(title=f"Stock Price and 5-Day Moving Avg for {ticker}",
                          xaxis_title="Date", yaxis_title="Price",
                          template='plotly_white')

        # Show the plot
        fig.show()

if __name__ == "__main__":
    finance = Finance()
    finance.get_moving_avg("KO")  # Example for Coca-Cola (KO). You can change this to any ticker symbol.
