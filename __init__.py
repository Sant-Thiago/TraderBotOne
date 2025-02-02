# from service.external.MetaTrader import MetaTrader
from datetime import datetime, timedelta
# from service.data.treatment import get_uptrend, get_downtrend
import pandas as pd
import plotly.graph_objects as go
from service.data.Analysis import Analysis
from dotenv import load_dotenv
import time
import os

# Carrega as variáveis do arquivo .env 
load_dotenv()

in_market = False

def buy(data, anls):
    if anls.strength >= 2:
        if anls.market is None:
            anls.market = anls.type.market.BULL
            anls.value = data.copy()
            anls.value['close'] += 20
            anls.value['low'] -= 20
            # anls.value['bottom_low'] = anls.bottom['low'] - 50
            input(f'compra: {anls.value}: ')

        # Se está comprado no mercado
        if anls.market == anls.type.market.BULL:
            anls.value['top_high'] = anls.top['high'] + 50
            print(f'ajuste compra: {anls.value}')

def sell(data, anls):
    if anls.strength <= -2:        
        if anls.market is None:
            anls.market = anls.type.market.BEAR
            anls.value = data.copy()
            anls.value['close'] -= 20
            anls.value['high'] += 20
            # anls.value['top_high'] = anls.top['high'] + 50
            input(f'vende: {anls.value}: ')

        # Se está vendido no mercado
        if anls.market == anls.type.market.BEAR:
            anls.value['bottom_low'] = anls.bottom['low'] - 50
            print(f'ajuste venda: {anls.value}')


def show(df):

    # Criar um gráfico de candlestick com Plotly
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["time"],
                open=df["open"],
                high=df["high"],
                low=df["low"],
                close=df["close"],
                name="Candlestick"
            )
        ]
    )

    # Personalizar layout
    fig.update_layout(
        title="Gráfico de Candlestick - Plotly",
        xaxis_title="Tempo",
        yaxis_title="Preço",
        xaxis_rangeslider_visible=False  # Oculta o range slider
    )

    # Exibir o gráfico
    fig.show()


def main():
    # login = int(os.getenv('LOGIN'))
    # server = os.getenv('SERVER')
    # password = os.getenv('PASSWORD')

    # mt = MetaTrader(login, server, password)
    # connected = mt.connect()

    # symbol = 'WING25'
    # test_start_date = datetime(2025, 1, 17, 0, 0, 0)
    # test_end_date = test_start_date + timedelta(days=1)
    # start_date = datetime(datetime.now().year, datetime.now().month, datetime.now().day, 0, 0, 0)
    
    # data = mt.get_data_for_period(symbol, start_date) 
    # df = pd.DataFrame(data)
    # df['time'] = pd.to_datetime(df['time'], unit='s')
    # df.to_csv('data.csv', index=False)
    
    df = pd.read_csv('data.csv')
    show(df)

    anls = Analysis()
    is_permited = False
    previous_data = None
    connected = df is not None

    # while connected:
    for i in range(len(df)):
        
        # print(df)

        # previous_data = df.iloc[-2]
        # previous_data_index = df.index[-2]
        
        if i == 0:
            continue

        # if df.size <= 2:
        #     continue

        previous_data = df.iloc[i - 1]
        previous_data_index = df.index[i - 1]

        # actual_data = df.iloc[-1]
        
        if anls.id == previous_data_index: 
            continue

        anls.id = previous_data_index

        # Se o candle anterior for UP
        if previous_data['open'] < previous_data['close'] :

            # Se a força estiver maior que zero, ou seja, se tiver mais de um candle positivo
            if anls.strength > 0:
                # Define a tendência de alta
                anls.trend = anls.type.trend.UP
            
            # Se a tendência anterior era de baixa
            if anls.trend == anls.type.trend.DOWN:
                # Se a força da tendência for forte
                if anls.strength < -1:
                    # define o fundo
                    anls.bottom = previous_data

                # Define a tendência de lateral
                ## Tira um ponto de força
                anls.trend = anls.type.trend.SIDEWAYS

            ## Se a tendência anterior era lateral ou alta
            ## else:         
            # Adiciona um ponto de força
            anls.strength = anls.more(1)
            
            buy(previous_data, anls)
        # Se o candle anterior for negatívo
        elif previous_data['open'] > previous_data['close']:

            # Se a força estiver menor que zero, ou seja, se tiver mais de um candle negativo
            if anls.strength < 0:
                # Define a tendência de baixa
                anls.trend = anls.type.trend.DOWN
            
            # Se a tendência anterior era de alta
            if anls.trend == anls.type.trend.UP:
                # Se a força da tendência for forte
                if anls.strength > 1:
                    # Define um topo
                    anls.top = previous_data

                # Define a tendência de lateral
                ## Tira um ponto de força
                anls.trend = anls.type.trend.SIDEWAYS


            ## Se a tendência anterior era lateral ou baixa
            ## else:         
            # Tira um ponto de força
            anls.strength = anls.minus(1)
            
            sell(previous_data, anls)
        # Se não há diferença entre a abertura e o fechamento 
        elif previous_data['open'] == previous_data['close']:
            # Define o meio do corpo que é indeciso
            middle = previous_data['open'] | previous_data['close']
            
            # Se a diferença da máxima for maior que a diferença da mínima  
            if previous_data['high'] - middle > middle - previous_data['low']:
                # Define a força como -1
                anls.strength = anls.minus(1)
                sell(previous_data, anls)

            # Se a diferença da mínima for maior que a diferença da máxima
            elif previous_data['high'] - middle < middle - previous_data['low']:
                # Define a força como +1
                anls.strength = anls.more(1)
                buy(previous_data, anls)

            # Se não a diferença entre a máxima e a mínima                           
            else:
                # Define a tendência como lateral
                anls.trend = anls.type.trend.SIDEWAYS

                # Se a tendência era de alta
                if anls.trend == anls.type.trend.UP:
                    anls.strength = anls.minus(1)
                    sell(previous_data, anls)

                # Se a tendência era de baixa
                elif anls.trend == anls.type.trend.DOWN:
                    anls.strength = anls.more(1)
                    buy(previous_data, anls)
                              
        print(anls)
        print('\n\n')
        time.sleep(5)

        ## 

    # mt.disconnect()

if __name__ == '__main__':
    main()



