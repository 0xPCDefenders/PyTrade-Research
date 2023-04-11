import tkinter as tk
import client as cli


# The application GUI.
class Application(tk.Tk):

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("PyTrade")
        self.geometry("250x250")

        # enter ticker
        ticker_instructions = tk.Label(self, text="Enter a stock ticker: ")
        ticker_instructions.pack(padx=0, pady=0)
        ticker_entry = tk.Entry(self, width=6)
        ticker_entry.pack(padx=15, pady=0)

        # fibonacci config
        option_list = ["0.236", "0.382", "0.5", "0.618", "0.786"]

        # enter ticker
        fib_instructions = tk.Label(self, text="Select a fibonacci ratio:")
        fib_instructions.pack(padx=1, pady=10)
        option_value = tk.StringVar(self)
        option_value.set(option_list[0])
        opt = tk.OptionMenu(self, option_value, *option_list)
        opt.pack(padx=1, pady=4)

        # get trades
        get_trades = tk.Button(self, text="Get Trades",
                               command=lambda: cli.main(ticker_entry.get(),
                                                        option_list.index(option_value.get())))

        get_trades.pack(pady=15)


app = Application()
app.mainloop()
