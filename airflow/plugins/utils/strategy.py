import pandas as pd
import numpy as np
from utils import db


def cross_sma_strategy(
        sma_short: int,
        sma_long: int,
        data: pd.DataFrame,
) -> pd.DataFrame:
    data['sma_short'] = data['close'].rolling(sma_short).mean()
    data['sma_long'] = data['close'].rolling(sma_long).mean()

    data['position'] = np.where(data['sma_short'] > data['sma_long'], 1, -1)

    return data[['time', 'position']].tail(1).assign(strategy_type='sma')


def bollinger_bands_strategy(
        data: pd.DataFrame,
        sma: int,
        dev: int
) -> pd.DataFrame:
    data['sma'] = data['close'].rolling(sma).mean()
    std = data['close'].rolling(sma).std() * dev
    data['lower'] = data['sma'] - std
    data['upper'] = data['sma'] + std

    data['distance'] = data['close'] - data['sma']
    data['position'] = np.where(data['close'] < data['lower'], 1, np.nan)
    data['position'] = np.where(data['close'] > data['upper'], -1, data['position'])
    data['position'] = np.where(data['distance'] * data['distance'].shift(1) < 0, 0, data['position'])
    data['position'] = data['position'].ffill().fillna(0)

    return data[['time', 'position']].tail(1).assign(strategy_type='bollinger ')