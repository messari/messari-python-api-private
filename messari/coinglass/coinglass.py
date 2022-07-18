"""This module is meant to contain the coinglass class"""

import pandas as pd
import requests

from messari.dataloader import DataLoader

from typing import List

class coinglass(DataLoader):
    """
    This class is a wrapper around the coinglass API
    """

    def __init__(self):
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)
        
    def get_symbols(self) -> List:
        url = 'https://fapi.coinglass.com/api/support/symbol'
        response = requests.get(url).json()
        symbols = response.get('data')
        return symbols
        
    def get_funding_rate(self, slug: str, type_in: str='U', interval: str='h8') -> pd.DataFrame:
        parameters = {
            'symbol': slug,
            'type': type_in,
            'interval': interval,
        }
        url = 'https://fapi.coinglass.com/api/fundingRate/v2/history/chart'
        response = requests.get(url, params=parameters).json()
        df = pd.DataFrame(response['data']['frDataMap'])
        df['price'] = response['data']['priceList']
        df.index = response['data']['dateList']
        df.index = pd.to_datetime(df.index,unit='ms')
        return df

    def get_open_interest(self, slug: str, time_type: int=0, exchange_name: str ='', currency: str='USD', type_in: int=0) -> pd.DataFrame:
        parameters = {
            'symbol': slug,
            'timeType': time_type,
            'exchangeName': exchange_name,
            'currency': currency,
            'type': type_in,
        }
        url = 'https://fapi.coinglass.com/api/openInterest/v3/chart?symbol=BTC&timeType=0&exchangeName=&currency=USD&type=0'
        url = 'https://fapi.coinglass.com/api/openInterest/v3/chart'
        response = requests.get(url, params=parameters).json()
        df = pd.DataFrame(response['data']['dataMap'])
        df['price'] = response['data']['priceList']
        df.index = response['data']['dateList']
        df.index = pd.to_datetime(df.index,unit='ms')
        return df

    def get_liquidations(self, slug: str) -> pd.DataFrame:
        url = 'https://fapi.coinglass.com/api/futures/liquidation/chart?symbol=BTC'
        response = requests.get(url).json()
        df = pd.DataFrame(response['data'])


        # unpack exchanges
        exchanges_raw = pd.DataFrame(df['list'].tolist())
        df_list = []
        names = []
        for col in exchanges_raw.columns:
            sub_df = pd.DataFrame(exchanges_raw[col].tolist())
            sub_df.exchange_name = sub_df.loc[0,'exchangeName'] #metadata
            df_list.append(sub_df)

        # For the main df
        df = df.drop(labels=['list'],axis=1,errors='ignore')
        df.exchange_name = 'combined'
        df_list.append(df)

        exchanges = pd.concat(df_list,axis=1,keys=[df.exchange_name for df in df_list])
        return exchanges
