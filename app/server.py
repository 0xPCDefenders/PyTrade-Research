import flask as fl
from flask import request
import yfinance as yf
import numpy as np
import json

app = fl.Flask(__name__)


# calculating the fibonacci retracement levels
def fibonacci(ticker_data, ratio_index):
    # extract closing prices from data
    ratios = [0.236, 0.382, 0.5, 0.618, 0.786]
    prices = []
    for i in range(0, len(ticker_data)):
        prices.append(ticker_data['Close'][i])

    # calculate Fibonacci retracement levels
    high_price = max(prices)
    low_price = min(prices)
    diff = high_price - low_price
    index = int(ratio_index)
    retracement = high_price - (ratios[index] * diff)
    return retracement


# Mean Reversion Backtest
def m_reversion_backtest(ticker, ratio_index, max_weeks, additional_weeks):
    # initializing variables
    start = 0
    end = 0
    stocks = 0
    portfolio = 100000
    time = []
    price = []
    position = []
    trades = []
    # the end of the data is up to a week maximum which represents the 6 month period
    while end <= max_weeks:
        new_data = ticker.history(interval="1wk", period="6mo")
        # additional weeks of data are added on every loop
        end = end + additional_weeks
        new_data = new_data[:end]
        m_1 = new_data['Close'].rolling(window=1).mean()
        m_2 = new_data['Close'].rolling(window=2).mean()
        # to drop null values due to yahoo finance's bad API(lol)
        m_1 = m_1.dropna()
        m_2 = m_2.dropna()

        # calculate the fibonacci retracement levels
        # calculate the mean of the entire historical data
        mean = np.mean(new_data['Close'])
        fib = fibonacci(new_data, ratio_index)
        support_resistance = (mean + fib) / 2

        if m_1[-1] > support_resistance:
            if stocks > 0:
                stocks = stocks - 1
                portfolio = portfolio + new_data['Close'][-1]
                time.append(end)
                price.append(new_data['Close'][-1])
                position.append(False)
                trades.append("Sold Tesla Stock @ $" + str(new_data['Close'][-1]))
                print("Sold Tesla Stock @ $", new_data['Close'][-1])
        if m_1[-1] < support_resistance:
            stocks = stocks + 1
            portfolio = portfolio - (new_data['Close'][-1])
            time.append(end)
            price.append(new_data['Close'][-1])
            position.append(True)
            trades.append("Bought Tesla Stock @ $" + str(new_data['Close'][-1]))
            print("Bought Tesla Stock @ $", new_data['Close'][-1])

    print("Realized P/L: ", portfolio - 100000, "\n")
    print("Unrealized P/L: ", (portfolio + (new_data['Close'][-1] * stocks)) - 100000)
    return time, price, position, trades


@app.route("/home")
def index():
    ticker = request.args.get("ticker")
    fib_ratio = int(request.args.get("fib_ratio"))
    data_ticker = yf.Ticker(ticker)
    time, price, position, trades = m_reversion_backtest(data_ticker, fib_ratio, 26, 4)
    graph = {
        "time": time,
        "price": price,
        "position": position,
        "trades": trades
    }
    graph_json = json.dumps(graph)
    return graph_json


if __name__ == "__main__":
    app.run()
