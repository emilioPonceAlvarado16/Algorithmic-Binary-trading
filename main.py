

############################################
################### MAIN ################### 
############################################

import time
# import logging
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import userdata
from iqoptionapi.stable_api import IQ_Option
# from iqoptionapi.support_resistance import support_and_resistance
from datetime import datetime
import mhi
import rainbow_strategy
# from iqoptionapi.strategies.mhi2 import mhi
# from iqoptionapi.strategies.tendencia import tendencia


#user = userdata.mainUser
Iq=IQ_Option("YourUsername","YourPassword")
check, reason = Iq.connect()

MODE = "PRACTICE" # REAL
Iq.change_balance(MODE)

# goal="EURUSD-OTC"
# goal="EURJPY-OTC"
# goal="EURJPY"
goal="EURUSD"
timeframe = 60
# expiration_mode = 1
cant_candles = 200
cont = 0
timer = 0
order_flag = 0

def get_data(candles_amount, goal):
    global timeframe
    df = pd.DataFrame()
    candles = []
    candles = Iq.get_candles(goal,timeframe,candles_amount,time.time())
    df = pd.concat([pd.DataFrame(candles), df], ignore_index=True )
    return df

def check_order (order_check, order_id):
    if order_check:
        result = Iq.check_binary_order(order_id)
        print('result is: ',result)
        if result['result']:
            res = round(float(result['profit_amount']) - float(result['amount']), 2)
            print("Resultado: ", res)
            
def is_time ():
    minutos = float(((datetime.now()).strftime('%M.%S'))[1:])
    # segundos = float(((datetime.now()).strftime('%S')))
    # print('minutos son: \n', minutos)
    # print('segundos son: \n', segundos)
    enter = False
    if minutos == 4.58 or minutos == 9.58:
        enter = True
    # if segundos == 28.00 or segundos == 58.0:
    # if segundos == 58.0:
    #     enter = True
    return enter

mercados=["EURUSD", "EURJPY","USDJPY"]

def mercadear(Iq,mercado, lista_binaria, indice): #cada hilo ejecutara esta funcion en paralelo
    
    data = get_data(200, mercado)
    opened = data ['open']
    closed = data ['close']
    trend = tendencia(data)
    signal,expiration_mode = mhi(opened, closed)
    print("Mercado: ", mercado)
    print('MHI: ', signal)
    print('trend: ', trend)
    if signal is not None and signal == trend:
        print('operando \n')
        order_check, order_id = Iq.buy(1, goal, signal, expiration_mode)
        lista_binaria[indice]=1
    else:
        lista_binaria[indice]=0
                #lista binaria para obtener si hubo señal y asi contar
                # se hace esto porque esta libreria no devuelve valor y una lista para evitar condicion de carrera
        
        
            
                

print("get candles")


try: 
    while True:
    	  #cada iteracion se crean y se destruyen hilos // New threads born and die in each iteration.
    	  
    	  num_mercados=len(mercados)
         
    	  lista_binaria=[None]*num_mercados
          

          
    	#   hilos=[None]*num_mercados
    	  
    	  if is_time():
        	   
            print('\n Analizando...')
            
            for i in range(num_mercados):
              mercadear(Iq, mercados[i], lista_binaria, i)
            #   hilos[i]=Thread(target=mercadear, args=(Iq, mercados[i],lista_binaria,i))
            #   hilos[i].start()  #empezar a ejecutar los hilos
            
            # for i in range(num_mercados):
            #   hilos[i].join() #esperar a que terminen
              
              #contar cuantas operaciones hicieron
            for operacion in lista_binaria:
              cont+=operacion
				  
              if cont == 10:
                #portafolio(Iq, cont)
                cont = 0  
                               	
            print('contador es: ',cont)	
            	
           
            #rainbow strategy / hilos
            time.sleep(5)
except KeyboardInterrupt:
    print('deteniendo...')
