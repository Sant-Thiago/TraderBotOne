from service.external.MetaTrader import MetaTrader
from datetime import datetime, timedelta
from service.data.treatment import get_uptrend, get_downtrend
import pandas as pd
from service.data.Analysis import Analysis


def main():
    mt = MetaTrader(login, server, password)
    connected = mt.connect()

    symbol = 'WING25'
    test_start_date = datetime(2025, 1, 17, 0, 0, 0)
    test_end_date = test_start_date + timedelta(days=1)
    start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)
    
    # while connected:
    data = mt.get_data_for_period(symbol, test_start_date, test_end_date) 
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')

    analysis = Analysis()
    previous_data = None

    for i in range(0, len(df)):
        if previous_data is None:
            previous_data = df.iloc[i]
            print(df.head(1))
            mt.disconnect()
            exit()
            continue
        
        actual_data = df.iloc[i]
        
        if previous_data['open'] < previous_data['close']:
            if actual_data['open'] < actual_data['close']:
                if previous_data['close'] < actual_data['close']:
                    analysis.set_trend('Uptrend')
                    # if previous_data['close'] < actual_data['close']
        elif previous_data['open'] > previous_data['close']:
            print('algo')
        analysis.status
        
    mt.disconnect()




