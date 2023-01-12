from binance.client import Client
from binance.enums import *
# import plotly.express as px
from plyer import notification
import pandas as pd
import numpy as np
import time


def get_hourly_dataframe():
    
    bars = um_futures_client.futures_klines(symbol=symbol, interval=interval, start_str = "60 minutes ago UTC")

    for x in bars:
        del x[5:]
   
    df = pd.DataFrame(bars, columns = ['date', 'open', 'high', 'low', 'close']).astype(np.float64)
    df['date'] = pd.to_datetime(df['date'],unit ='ms')
    sma_trade_logic(df)

# def polt_graph(df):

#     df[['ma9', 'EMA15']].plot()
#     plt.scatter(df.index,df['Buy'], color='blue' , label='Buy', marker='^')
#     plt.scatter(df.index,df['Sell'], color='red' , label='red', marker='v')
#     plt.xlabel('Date',fontsize = 16)
#     plt.ylabel('Close price',fontsize = 16)
#     plt.show()

def closeBuy(cl):
    
    global CloseBuyOrder
    CloseBuyOrder = um_futures_client.futures_create_order(
            symbol=symbol,
            type="MARKET",
            positionSide='LONG',
            side ='SELL',
            quantity= cl,
        )
    print (CloseBuyOrder)
    
def closeSell(cl):
    cl = abs(cl)
    print ('cl: ',cl)
    global CloseSellOrder
    CloseSellOrder = um_futures_client.futures_create_order(
            symbol=symbol,
            type="MARKET",
            positionSide='SHORT',
            side ='BUY',
            quantity= cl,
        )
    print (CloseSellOrder)

def close(um_futures_client):
    sellP = 0
    BuyP = 0 
    xk = um_futures_client.futures_position_information(symbol='ETHUSDT')
    for future in xk:
        amount = future["positionAmt"]
        if float(amount) < 0 and amount != 0:
            print ('amount: ', amount)
            sellP = amount
        if float(amount) > 0 and amount != 0:
            print ('amount: ', amount)
            BuyP = amount
    print('sell point: ', sellP, 'buy point: ', BuyP)
    if sellP != 0:
        closeSell(float(sellP))
    if BuyP != 0:
        closeBuy(float(BuyP))
                    

def open_Buy_order(um_futures_client, point):
    print('Buy with', first_entry_percent) 
    print ('quantity= ',point)
    # notification.notify(
    # title = 'open long position',
    # message = 'first position',
    # app_icon = None,
    # timeout = 20,
    #             )

    global BuyOrder
    BuyOrder = um_futures_client.futures_create_order(
        symbol=symbol,
        type='MARKET',
        positionSide='LONG',
        side ='BUY',
        quantity= point,        
        )
    print(BuyOrder)

    
def open_Sell_order(um_futures_client, point):
    print('Sell with',first_entry_percent)
    print ('quantity= ',point)
    # notification.notify(
    # title = 'open short position',
    # message = 'first position',
    # app_icon = None,
    # timeout = 10,
    #                 )
    global SellOrder
    SellOrder = um_futures_client.futures_create_order(
            symbol=symbol,
            type="MARKET",
            positionSide='SHORT',
            side ='SELL',
            quantity= point,
            
        )
    print (SellOrder)

def open_BUY_order_Two(um_futures_client,Coeficiente):
    print('BUY with',Coeficiente)
    print('quantity= ',point2)
    # notification.notify(
    # title = 'open long position',
    # message = 'long position with',
    # app_icon = None,
    # timeout = 20,
    # )
    BuyOrder =  um_futures_client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            positionSide='LONG',
            side ='BUY',
            quantity= point2,
        )
    print (BuyOrder)

    
def open_SELL_order_Two(um_futures_client,Coeficiente):
        print('SELL with',Coeficiente) 
        print ('quantity= ',point2)
        # notification.notify(
        # title = 'open sell position',
        # message = 'short position with',
        # app_icon = None,
        # timeout = 10,
        #                 )
  
        SellOrder = um_futures_client.futures_create_order(
            symbol=symbol,
            type='MARKET',
            positionSide='SHORT',
            side ='SELL',
            quantity= point2,
            callbackRate=2.0
        )
        print(SellOrder)   

def TpBuy(lastSig):
    global tp
    tp = ((lastSig * BUYprofit )/1000)
    return tp
def FirstPositon(CurrentPrice,volume):
    global point
    point = (((volume * first_entry_percent)/100)/CurrentPrice['lastPrice'])
    point = round(point,3)
    return point
def SecondPostion(Coeficiente_X):
    global point2
    point2 = Coeficiente_X * point
    print ('p: ' , point2)
    point2 = round(point2, 3)
    # global total_point
    # total_point = point + point2
    # print ('total quantity: ', total_point)
    return point2

def Buy_or_sell(buy_sell_list,i, tp):
 for index, value in enumerate(buy_sell_list):
        CurrentPrice = um_futures_client.futures_ticker(symbol=symbol)
        # CurrentPrice['lastPrice'] = float(CurrentPrice['lastPrice'])
        CurrentPrice['lastPrice'] = float(input('enter the price'))
        print(CurrentPrice['lastPrice'])
        print (value)
        if value == 2.0:
            # if CurrentPrice['lastPrice'] < df['Buy'][index]:
            if i[-1] == 200 or i == ['']:
                state = 100
                i.append(state)
                # print(i)
                sig.append(CurrentPrice['lastPrice'])
                counting = len(sig)
                print(sig[len(sig) - 1])
                lastSig = sig[-1]
                tp = TpBuy(lastSig)
                print('tp=', tp)
                if counting > 0 and counting < 2:              
                    F_point = FirstPositon(CurrentPrice,volume)
                    open_Buy_order(um_futures_client,F_point)
                elif counting > 1 and counting < 3:
                    Coeficiente_X = 3.09
                    point2 = SecondPostion(Coeficiente_X)
                    open_BUY_order_Two(um_futures_client,Coeficiente_X)
                elif counting > 2 and counting < 4:
                    Coeficiente_X = 6.44
                    point2 = SecondPostion(Coeficiente_X)
                    open_BUY_order_Two(um_futures_client,Coeficiente_X)
                elif counting >= 4:
                    print('more than 3 times loop --- closing')
                    exit()
        if value == -2.0:
            # if CurrentPrice ['lastPrice'] > df['Sell'][index]:
            if i == [''] or i[-1] == 100:
                state = 200
                i.append(state)
                # print(i)
                sig.append(CurrentPrice['lastPrice'])
                print(sig)
                counting = len(sig)
                lastSig = sig[-1]
                tp = ((lastSig * SELLprofit )/1000)
                print('tp=', tp)       
                if counting > 0 and counting < 2:              
                    F_point = FirstPositon(CurrentPrice,volume)
                    open_Sell_order(um_futures_client, point)
                elif counting > 1 and counting < 3:
                    Coeficiente_X = 3.09
                    point2 = SecondPostion(Coeficiente_X)
                    open_SELL_order_Two(um_futures_client,Coeficiente_X)
                elif counting > 2 and counting < 4:
                    Coeficiente_X = 6.44
                    point2 = SecondPostion(Coeficiente_X)
                    open_SELL_order_Two(um_futures_client,Coeficiente_X)
                elif counting >= 4:
                    print('more than 3 times loop --- closing')
                    exit()
        print ('i: ',i ,'tp: ', tp)
        if i[-1] == 100 and CurrentPrice['lastPrice'] > float(tp):
            del sig[0:]
            counting = 0
            tp = 0
            del i[0:]
            x = ''
            i.append(x)
            close(um_futures_client)
            print ('close close close')
        if i[-1] == 200 and CurrentPrice['lastPrice'] < float(tp):
            del sig[0:]
            counting = 0
            tp = 0
            del i[0:]
            x = ''
            i.append(x)
            close(um_futures_client)
            print ('close close close')
            
        # if sig != '':
        #     for b1 in account['assets']:
        #         if b1['asset'] == 'USDT':
        #             initialmargin = float(b1['initialMargin'])
        #             unrealizedprofit = float(b1['unrealizedProfit'])
        #             pnl=float(b1['crossUnPnl'])
        #             roe = unrealizedprofit / initialmargin*100
        #     print('PNL: '+str(pnl)+'USDT')
        #     print('ROE: '+str(roe)+'%')
                        


def sma_trade_logic(symbol_df):
    
    symbol_df.set_index('date' ,inplace=True)
    symbol_df.index = pd.to_datetime(symbol_df.index, unit='ms').tz_localize("UTC").tz_convert('Asia/Tbilisi')
    
    # symbol_df['ma9'] = (((symbol_df['high'] + symbol_df['low'])+ symbol_df['close']*2)/4).rolling(24).mean().shift(periods=-15, fill_value=0).astype(np.float64)
    symbol_df['ma9'] = (symbol_df['close']).rolling(24).mean().astype(np.float64).shift(periods=-15, fill_value=0)

    # dx = symbol_df['ma9'].shift(15)
    # symbol_df['Nma9'] = dx
    symbol_df = symbol_df[:-15]
    # symbol_df['EMA15'] = (((symbol_df['high'] + symbol_df['low'])+ symbol_df['close']*2)/4).ewm(span=39 , adjust=False).mean().astype(np.float64)
    symbol_df['EMA15'] = (symbol_df['close']).ewm(span=39 , adjust=False).mean().astype(np.float64)
    symbol_df['signal'] = np.where(symbol_df['ma9'] > symbol_df['EMA15'] ,2,0)
    
    symbol_df['Position'] = symbol_df['signal'].diff()
    
    symbol_df['Buy'] = np.where(symbol_df['Position'] == 2, symbol_df['close'], np.NaN)
    symbol_df['Sell'] = np.where(symbol_df['Position'] == -2, symbol_df['close'], np.NaN)
    
    with open('output.txt', 'w')as f:
        f.write(
            symbol_df.to_string()
        )
    # print(symbol_df['Position'])
    tp = 0
    buy_sell_list = symbol_df['Position'][:-1].tolist()
    print(buy_sell_list)
    Buy_or_sell(buy_sell_list,i, tp)
    
   
if __name__ == '__main__':
    
    um_futures_client = Client()

    
    key = '2WOk3zWe1F1KCnSgXNXhRvXdcaAaPz8vpQ3Yqk3DBdRtTbY39j0kDPZVkO1Sicf1'
    secret = 'JTyQlmcGtTEdOQVim4bTLtoCs2ahkWTKVVDeNMpocI7PbzHZfFJo5eEVOWHJkHns'
    um_futures_client = Client(key, secret)
    balance = um_futures_client.futures_account_balance(asset="USDT")

    for check_balance in balance:
        if check_balance["asset"] == "USDT":
            usdt_balance = check_balance["balance"]
            
    volume = float(usdt_balance)
    # starttime = '8 day ago UTC'
    interval = '1m'
    timeframe = '1m'

    BUYprofit = 1003.2
    SELLprofit = 996.8
    global first_entry_percent
    first_entry_percent = float(input('Enter percent for first position: '))
    sig=[]
    global i
    i = ['']
    symbol = 'ETHUSDT'
        
while True:
    get_hourly_dataframe()
    time.sleep(15)