from service.external.MetaTrader import MetaTrader
from datetime import datetime, timedelta
from service.data.treatment import get_uptrend, get_downtrend
import pandas as pd
from service.data.anls import anls
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
    
    anls = anls()
    previous_data = None
    in_market = None
    
    data = mt.get_data_for_period(symbol, start_date) 
    df = pd.DataFrame(data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.to_csv('data.csv', index=False)

    is_permited = False;
    while connected:
        
        print(df)
        print('')

        previous_data = df.iloc[-2]
        if previous_data is None:
            continue 
        

        # if df.size < 3:
        #     continue;

        actual_data = df.iloc[-1]
        
        if anls.type
        if previous_data['open'] < previous_data['close']:
            anls.position = anls.type.position.POSITIVO
            anls.strength = anls.type.strength.ONE


        # Se o candle anterior for positivo e não estiver no mercado
        if previous_data['open'] < previous_data['close']: 
            # Se não estiver comprado no mercado
            ## ENTRETANTO DEVE-SE ASSEGURAR QUE ELE PODE TENTAR VENDER EM UMA POSIÇÃO DESVANTAJOSA
            if anls.in_market is not anls.type.in_market.COMPRADO:
                ## Aqui devese colocar uma ordem de compra 20 pontos acima da máxima, e um stop em 100 pontos abaixo da mínima
                anls.in_market = anls.type.in_market.COMPRADO
                anls.position = anls.type.position.POSITIVO
                anls.strengh += 1

            # Se não estiver vendido no mercado
            elif anls.in_market is not anls.type.in_market.VENDIDO:
                 ## Aqui devese colocar uma ordem de venda 20 pontos abaixo da mínima, e um stop em 100 pontos acima da máxima
                anls.in_market = anls.type.in_market.VENDIDO
                anls.position = anls.type.position.NEGATIVO
                anls.strengh += 1
            
            else:
                ## Não sei ainda
                

                              
            # Se o candle atual for positivo 
            if actual_data['open'] < actual_data['close']:
                if previous_data['close'] < actual_data['close']:
                    
                    if anls.trend == 'Uptrend':
                        anls.strength = 2
                        print('Entra comprado')
                        in_market = 'Comprado'
            
                    else:
                        anls.set_trend('Uptrend')
                        anls.set_status('Medium')
            
                    if previous_data['high'] < actual_data['close']:
                        anls.set_status('Strong')
            
                    if previous_data['high'] > actual_data['high']:
                        anls.set_status('Week')

            elif actual_data['open'] > actual_data['close']:
                anls.set_trend('Sideway')
                anls.set_status('Week')
        
        elif previous_data['open'] > previous_data['close'] and in_market != 'Vendido':
            if actual_data['open'] > actual_data['close']:
                if previous_data['close'] > actual_data['close']:
                    
                    if anls.get_trend() == 'Downtrend':
                        anls.set_status('Strong')
                        print('Entra vendido')
                        in_market = 'Vendido'
                    
                    else:
                        anls.set_trend('Downtrend')
                        anls.set_status('Medium')

                    if previous_data['low'] < actual_data['close']:
                        anls.set_status('Strong')

                    if previous_data['low'] > actual_data['low']:
                        anls.set_status('Week')

        print(anls)
        print('\n\n')
        time.sleep(1)

    mt.disconnect()

if __name__ == '__main__':
    main()



