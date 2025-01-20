import MetaTrader5 as mt5
import numpy as np
from datetime import datetime

class MetaTrader:
    """
    A class to interact with the MetaTrader platform via its API.
    """

    def __init__(self, login: int, server: str, password: str):
        """
        Initializes the connection to MetaTrader.

        :param login: Account ID.
        :param server: Server name.
        :param password: Account password.
        """
        self.login = login
        self.server = server
        self.password = password
        self.connected = False
        print('MetaTrader5 package version: ', mt5.__version__)

    def connect(self) -> bool:
        """
        Connects to MetaTrader.

        :return: True if connection is successful, False otherwise.
        """
        self.connected = mt5.initialize(login=11924496, server=self.server, password=self.password)
        if not self.connected:
            print('Connection failed, error code = ', mt5.last_error())
        return self.connected

    def disconnect(self):
        """
        Disconnects from MetaTrader.
        """
        if self.connected:
            mt5.shutdown()
            self.connected = False

    def get_account_info(self) -> mt5.AccountInfo:
        """
        Fetches account information.

        :return: An instance of mt5.AccountInfo containing account details, or None if failed.
        """
        account_info = mt5.account_info()
        if account_info is None:
            print(f'Failed to get account info, error code = {mt5.last_error()}')
        return account_info

    def get_symbols(self, quantity: int) -> mt5.SymbolInfo:
        """
        Fetches information about available symbols.

        :param quantity: Number of symbols to retrieve.
        :return: Symbol information for the first `quantity` symbols.
        """
        symbols = mt5.symbols_get()
        for symbol in symbols[:quantity]:
            print(type(symbol))
            return symbol

    def get_symbol_info(self, symbol: str) -> mt5.SymbolInfo:
        """
        Fetches information about a specific symbol.

        :param symbol: Name of the symbol.
        :return: An instance of mt5.SymbolInfo containing symbol details, or None if not found.
        """
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f'Symbol {symbol} not found. Error: {mt5.last_error()}')
            return None
        print(type(symbol_info))
        return symbol_info

    def get_symbol_tick(self, symbol: str) -> mt5.Tick:
        """
        Fetches the latest tick information for a symbol.

        :param symbol: Name of the symbol.
        :return: An instance of mt5.Tick containing tick data, or None if not found.
        """
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f'Tick data for {symbol} not found. Error: {mt5.last_error()}')
            return None
        print(type(tick))
        return tick

    def get_ticks_for_period(self, symbol: str, start_date: datetime, end_date: datetime = datetime.now()) -> np.ndarray:
        """
        Fetches tick data for a symbol within a specified time period.

        :param symbol: Name of the symbol.
        :param start_date: Start datetime for the data.
        :param end_date: End datetime for the data.
        :return: A numpy.ndarray containing tick data, or an empty array if no data is found.
        """
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        ticks = mt5.copy_ticks_range(symbol, start_timestamp, end_timestamp, mt5.COPY_TICKS_ALL)

        if ticks is None or len(ticks) == 0:
            print(f'No tick data found for {symbol} between {start_date} and {end_date}')
            return np.array([])

        return ticks

    def get_data_for_period(self, symbol: str, start_date: datetime, end_date: datetime = datetime.now()) -> np.ndarray:
        """
        Fetches candlestick data for a symbol within a specified time period.

        :param symbol: Name of the symbol.
        :param start_date: Start datetime for the data.
        :param end_date: End datetime for the data.
        :return: A numpy.ndarray containing candlestick data, or an empty array if no data is found.
        """
        start_timestamp = int(start_date.timestamp())
        end_timestamp = int(end_date.timestamp())

        rates = mt5.copy_rates_range(symbol, mt5.TIMEFRAME_M1, start_timestamp, end_timestamp)

        if rates is None or len(rates) == 0:
            print(f'No data found for {symbol} in the specified period')
            return np.array([])

        return rates
