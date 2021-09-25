


def mhi (opened, closed):
    """
    ********* analiza las 3 ultimas velas, determina cual es la minoria y 
    devuelve como señal put si la siguiente vela sera roja o call si sera verde

    """
    last_3_open = opened.tail(3)
    last_3_close = closed.tail(3)
    
    r = 0
    g = 0
    doji = 0
    for idx, val in enumerate(last_3_open):
        print('open is {}, close is {}'.format(last_3_open.iloc[idx], last_3_close.iloc[idx]))
        if last_3_open.iloc[idx] > last_3_close.iloc[idx]:
            r += 1 
            print('red\n')
        elif last_3_open.iloc[idx] < last_3_close.iloc[idx]:
            g += 1 
            print('green\n')
        else:
            doji += 1
            print('doji\n')
    
    signal = None
    if doji == 0:
        if g >=2:
            signal = 'put'
        if r >=2:
            signal = 'call'
    print(f'R:{r} G:{g} D:{doji}')
    return signal
    
