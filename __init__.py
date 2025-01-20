from service.external.MetaTrader import MetaTrader
from datetime import datetime, timedelta
from service.data.treatment import get_uptrend, get_downtrend
import pandas as pd
from service.data.Analysis import Analysis
from dotenv import load_dotenv
import time
import os

# Carrega as variáveis do arquivo .env 
load_dotenv()

def main():
    login = int(os.getenv('LOGIN'))
    server = os.getenv('SERVER')
    password = os.getenv('PASSWORD')

    mt = MetaTrader(login, server, password)
    connected = mt.connect()

    symbol = 'WING25'
    test_start_date = datetime(2025, 1, 17, 0, 0, 0)
    test_end_date = test_start_date + timedelta(days=1)
    start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)
    
    analysis = Analysis()
    previous_data = None
    in_market = None
    
    data = mt.get_data_for_period(symbol, start_date) 
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.to_csv('data.csv', index=False)
    while connected:
        
        print(df)
        print('')

        prev = df.iloc[-3]
        if not prev.equals(previous_data):
            previous_data = prev
            continue
        
        actual_data = df.iloc[-2]
        
        if previous_data['open'] < previous_data['close'] and in_market != 'Comprado':
            if actual_data['open'] < actual_data['close']:
                if previous_data['close'] < actual_data['close']:
                    
                    if analysis.get_trend() == 'Uptrend':
                        analysis.set_status('Strong')
                        print('Entra comprado')
                        in_market = 'Comprado'
            
                    else:
                        analysis.set_trend('Uptrend')
                        analysis.set_status('Medium')
            
                    if previous_data['high'] < actual_data['close']:
                        analysis.set_status('Strong')
            
                    if previous_data['high'] > actual_data['high']:
                        analysis.set_status('Week')

            elif actual_data['open'] > actual_data['close']:
                analysis.set_trend('Sideway')
                analysis.set_status('Week')
        
        elif previous_data['open'] > previous_data['close'] and in_market != 'Vendido':
            if actual_data['open'] > actual_data['close']:
                if previous_data['close'] > actual_data['close']:
                    
                    if analysis.get_trend() == 'Downtrend':
                        analysis.set_status('Strong')
                        print('Entra vendido')
                        in_market = 'Vendido'
                    
                    else:
                        analysis.set_trend('Downtrend')
                        analysis.set_status('Medium')

                    if previous_data['low'] < actual_data['close']:
                        analysis.set_status('Strong')

                    if previous_data['low'] > actual_data['low']:
                        analysis.set_status('Week')

        print(analysis)
        print('\n\n')
        time.sleep(1)

    mt.disconnect()

if __name__ == '__main__':
    main()



