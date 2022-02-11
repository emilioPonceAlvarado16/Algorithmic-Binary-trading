



import time
# import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from iqoptionapi.stable_api import IQ_Option
from datetime import datetime
import threading

def order(signal,Iq,goal,expiration_mode,flag_order,contador):
    counter = contador
    if ((signal == 'put') or (signal == 'call')) and (flag_order == 0):
    # if signal is not None:
        print("operando....")
        print('signal is: {}, flag is {} \n', signal, flag_order)
        order_check, order_id = Iq.buy(1, goal, signal, expiration_mode)
        if order_check:
            flag_order =1
        # print('order_check is {}, order_id: {}'.format(order_check, order_id))
        # check_order(order_check, order_id)
        counter = counter + 1
        print('contador is: \n',counter)
    if ((signal != 'put') or (signal != 'call')) and (flag_order == 1):
        flag_order = 0
    if counter == 10:
                portafolio(Iq, counter)
                counter = 1
    return (counter,flag_order)

def buy_sell(datos):
    flag = -1
    sigPriceBuy = []
    sigPriceSell = []
    sig = 0
    signal = []
    
    for i in range(len(datos)):
        if (datos['EMA6'][i] > datos['EMA14'][i]) & (datos['EMA14'][i] > datos['EMA26'][i]) :
            if flag != 1:
                sigPriceBuy.append(datos['close'][i])
                sigPriceSell.append(np.nan)
                signal.append(np.nan)
                flag = 1
            elif (flag == 1) and (datos['close'][i] <= datos['EMA26'][i]):
                sigPriceBuy.append(datos['close'][i])
                sigPriceSell.append(np.nan)
                sig = 'call'
                # print('buy\n')
                # order(sig)
                signal.append(sig)
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
                signal.append(np.nan)
        elif (datos['EMA6'][i] < datos['EMA14'][i]) & (datos['EMA14'][i] < datos['EMA26'][i]) :
            if flag != 0:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(datos['close'][i])
                signal.append(np.nan)
                flag = 0
            elif (flag == 0) and (datos['close'][i] >= datos['EMA26'][i]):
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(datos['close'][i])
                sig = 'put'
                # print('sell\n')
                # order(sig)
                signal.append(sig)
            else:
                sigPriceBuy.append(np.nan)
                sigPriceSell.append(np.nan)
                signal.append(np.nan)
        else:
            sigPriceBuy.append(np.nan)
            sigPriceSell.append(np.nan)
            signal.append(np.nan)
    return (sigPriceBuy, sigPriceSell, signal)


def rainbow_strategy(data,Iq,goal,expiration_mode,order_flag,cont):
    buy_sell2 = []
    order_flag2 = 0
    cont2 = 1

    data['EMA6'] = data['close'].ewm(span=6,adjust=False).mean()
    data['EMA14'] = data['close'].ewm(span=14,adjust=False).mean()
    data['EMA26'] = data['close'].ewm(span=26,adjust=False).mean()
    
    data['grad1_6-14'] = abs((data['EMA14'] - data['EMA6']) * 1000000)
    data['grad1_14-26'] = abs((data['EMA26'] - data['EMA14']) * 1000000)
    
    
    data['from2'] = pd.to_datetime(data['from'],unit='s')
    data['at2'] = pd.to_datetime(data['at'],unit='ns')
    data['to2'] = pd.to_datetime(data['to'],unit='s')
    
    buy_sell2 = buy_sell(data)
    data['Buy_Signal_Price'] = buy_sell2[0]
    data['Sell_Signal_Price'] = buy_sell2[1]
    data['Signal'] = buy_sell2[2]
    signal = buy_sell2[2][-1]
    print('signal is: \n', signal)
    cont2, order_flag2 = order(signal,Iq,goal,expiration_mode,order_flag,cont)
    order_flag = order_flag2
        
