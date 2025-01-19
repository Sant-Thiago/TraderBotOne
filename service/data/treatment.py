import pandas as pd

def get_uptrend( actual_data: pd.Series, previous_data: pd.Series ):
    c = 0
    if previous_data['open'] < previous_data['close'] and actual_data['open'] < actual_data['close'] and previous_data['close'] <= actual_data['close']:
        c += 1
    else:
        c = 0
        top = 0
        if actual_data['low'] > previous_data['high']: top = actual_data['low']
        else: top = previous_data['high']

        print(f'tendencia de alta atingiu um topo {top} em {actual_data['time']}\n')

def get_downtrend( actual_data: pd.Series, previous_data: pd.Series ):
    c = 0
    if previous_data['open'] > previous_data['close'] and actual_data['open'] > actual_data['close'] and previous_data['close'] >= actual_data['close']:
        c += 1
    elif c > 0:
        c = 0
        top = 0
        if actual_data['low'] > previous_data['high']: top = actual_data['low']
        else: top = previous_data['high']

        print(f'tendencia de alta atingiu um topo {top} em {actual_data['time']}\n')

