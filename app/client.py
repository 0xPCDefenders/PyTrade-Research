import requests
import matplotlib.pyplot as plt
import numpy as np
import yfinance as yf


# the controller that sends requests to the server
def main(ticker_label, fib_ratio):
    # ticker_label = input("Enter a ticker: ")
    url = "http://localhost:5000/home"
    params = {
        "ticker": ticker_label,
        "fib_ratio": fib_ratio
    }
    response = requests.get(url, params=params)
    output = response.json()
    graph_display(ticker_label, output)


# displays graph of trades with API data
def graph_display(ticker, output):
    ticker_display = yf.Ticker(ticker)
    historical_data = ticker_display.history(interval="1wk", period="6mo")
    x = np.arange(0, 26)
    y = []

    for i in range(0, 26):
        y.append(historical_data['Close'][i])

    # plotting
    plt.title(f"{ticker} 6 month Historical Data")
    plt.xlabel("Time in Weeks")
    plt.ylabel("Price in Dollars")
    plt.plot(x, y, color="red")

    time = output["time"]
    price = output["price"]
    position = output["position"]

    for unit in range(0, len(time)):
        if position[unit]:
            plt.plot(time[unit], price[unit], color="red", marker=">", markersize=20,
                     markeredgecolor="green",
                     markerfacecolor="red")
        if not position[unit]:
            plt.plot(time[unit], price[unit], color="green", marker=">", markersize=20,
                     markeredgecolor="red",
                     markerfacecolor="green")

    plt.show()
