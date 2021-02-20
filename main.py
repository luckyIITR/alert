import yfinance as yf
import pandas as pd
from datetime import datetime
from bot import telegram_chatbot
bot = telegram_chatbot("config.cfg")
id = 965690681

reported = []

while True:
    alert_dic = {}


    def get_alert():
        df = pd.read_csv('alert_data.csv')
        df.dropna(inplace=True)
        df["Symbol"] = df["Symbol"] + ".NS"
        df.sort_values(by="Symbol", inplace=True)
        df.reset_index(drop="True", inplace=True)
        symbols = df['Symbol'].values
        symbols = list(symbols)
        df.set_index("Symbol", inplace=True)

        return df, symbols


    def get_LTP(df, symbols):

        data = yf.download(  # or pdr.get_data_yahoo(...
            # tickers list or string as well
            tickers=symbols,

            # use "period" instead of start/end
            # valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
            # (optional, default is '1mo')
            period="1d",
            end=datetime.now()

        )
        data = data['Close'].iloc[-1].to_frame().reset_index().sort_values(by="index").set_index("index")
        df = pd.concat([df, data], axis=1)
        if "LTP" in df.columns:
            df.drop(['LTP'], axis=1, inplace=True)
        df.rename(columns={df.columns[1]: "LTP"}, inplace=True)
        #     print(df)
        return df

    df, symbols = get_alert()

    df = get_LTP(df,symbols)
    signal = df['LTP'] - df['Alert Price']
    signal = signal.to_frame(name = "signal")
    alert_dic[datetime.now()]  = list(signal[signal.signal>0].index)

    if alert_dic:
        reply = f"Price Alert !!!\n{list(alert_dic.keys())[0]}"
        flag = 0
        for stock in alert_dic[list(alert_dic.keys())[0]]:
            if stock in reported:
                continue
            flag = 1
            reply = reply + "\n" + str(stock[:-3]) +"\n" + f"LTP : {round(df.loc[stock,'LTP'],2)}"
            reported.append(stock)
        if flag :
            bot.send_message(reply, id)
        alert_dic = {}



