"""
This module is meant to contain the CoinGecko class
Ref: https://www.coingecko.com/en/api/documentation
"""


# Global imports
import datetime
from string import Template
from typing import Union, List, Dict

import pandas as pd

from messari.dataloader import DataLoader

# Local imports
from messari.utils import validate_input, get_taxonomy_dict, time_filter_df
#from .helpers import format_df

##########################
# URL Endpoints
##########################
BASE_URL = 'https://api.coingecko.com/api/v3'

HEADERS = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }


class CoinGecko(DataLoader):
    """This class is a wrapper around the CoinGecko API
    """

    def __init__(self):
        # TODO add support for api key
        #messari_to_dl_dict = get_taxonomy_dict("messari_to_cg.json")
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)

    ## Coins
    def get_coin_list(self) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/list'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df

    def get_coin_markets(self, category: str=None, order: str=None, per_page: int=10, page: int=1) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/markets'
        parameters = {
                'vs_currency': 'usd',
                'per_page': per_page,
                'page': page
                }
        if order:
            parameters['order'] = order
        if category:
            parameters['category'] = category

        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df

    def get_coin(self, coin_id: str) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/{coin_id}'
        response = self.get_response(url)
        df = pd.Series(response).to_frame(name=coin_id)
        return df

    def get_coin_tickers(self, coin_id: str, page: int=1) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/{coin_id}/tickers'
        parameters = {
                'page': page,
                'depth': 'true'
                }

        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response['tickers'])
        return df

    def get_coin_history(self, coin_id: str, date: str) -> pd.DataFrame:
        """
        @param date: 'dd-mm-yyyy'
        """
        url = f'{BASE_URL}/coins/{coin_id}/history'
        parameters ={'date': date}
        response = self.get_response(url, params=parameters)
        df = pd.Series(response).to_frame(name=coin_id)
        return df

    def get_coin_chart(self, coin_id: str, days: str='max') -> pd.DataFrame:
        url = f'{BASE_URL}/coins/{coin_id}/market_chart'
        parameters = {
                'vs_currency': 'usd',
                'days': days
                }
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        df.index = df['prices'].apply(lambda x: x[0])
        df.index = pd.to_datetime(df.index, unit='ms')

        df['prices'] = df['prices'].apply(lambda x: x[1])
        df['market_caps'] = df['market_caps'].apply(lambda x: x[1])
        df['total_volumes'] = df['total_volumes'].apply(lambda x: x[1])
        return df

    def get_coin_range(self, coin_id: str, _from: int, to: int) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/{coin_id}/market_chart/range'
        parameters = {
                'vs_currency': 'usd',
                'from': _from,
                'to': to
                }
        response = self.get_response(url, params=parameters)

        df = pd.DataFrame(response)
        df.index = df['prices'].apply(lambda x: x[0])
        df.index = pd.to_datetime(df.index, unit='ms')

        df['prices'] = df['prices'].apply(lambda x: x[1])
        df['market_caps'] = df['market_caps'].apply(lambda x: x[1])
        df['total_volumes'] = df['total_volumes'].apply(lambda x: x[1])
        return df

    def get_coin_ohlc(self, coin_id: str, days: int=7):
        url = f'{BASE_URL}/coins/{coin_id}/ohlc'
        parameters = {
                'vs_currency': 'usd',
                'days': days
                }
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response).set_index(0)
        rename_dict = {
                1:'open',
                2:'high',
                3:'low',
                4:'close'
                }
        df.rename(columns=rename_dict,inplace=True)
        df.index = pd.to_datetime(df.index,unit='ms')
        return df

    ## Contract
    def get_contract(self, asset_platform: str, contract_address: str) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/{asset_platform}/contract/{contract_address}'
        response = self.get_response(url)
        df = pd.Series(response).to_frame(name=f'{asset_platform}_{contract_address}')
        return df

    def get_contract_market(self, asset_platform: str, contract_address: str, days: str='max') -> pd.DataFrame:
        url = f'{BASE_URL}/coins/{asset_platform}/contract/{contract_address}/market_chart'
        parameters = {
                'vs_currency': 'usd',
                'days': days
                }
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response)
        df.index = df['prices'].apply(lambda x: x[0])
        df.index = pd.to_datetime(df.index, unit='ms')

        df['prices'] = df['prices'].apply(lambda x: x[1])
        df['market_caps'] = df['market_caps'].apply(lambda x: x[1])
        df['total_volumes'] = df['total_volumes'].apply(lambda x: x[1])
        return df

    def get_contract_range(self, asset_platform: str, contract_address: str, _from: int, to: int) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/{asset_platform}/contract/{contract_address}/market_chart/range'
        parameters = {
                'vs_currency': 'usd',
                'from': _from,
                'to': to
                }
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response)
        df.index = df['prices'].apply(lambda x: x[0])
        df.index = pd.to_datetime(df.index, unit='ms')

        df['prices'] = df['prices'].apply(lambda x: x[1])
        df['market_caps'] = df['market_caps'].apply(lambda x: x[1])
        df['total_volumes'] = df['total_volumes'].apply(lambda x: x[1])
        return df

    ## Asset Platforms
    def get_asset_platforms(self) -> pd.DataFrame:
        url = f'{BASE_URL}/asset_platforms'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df

    ## Categories
    def get_categories_list(self) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/categories/list'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df

    def get_categories(self) -> pd.DataFrame:
        url = f'{BASE_URL}/coins/categories'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df

    ## Exchanges
    def get_exchanges(self, per_page: int=10, page: int=1) -> pd.DataFrame:
        url = f'{BASE_URL}/exchanges'
        parameters = {
                'per_page':per_page,
                'page': page
                }
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response)
        return df

    def get_exchanges_list(self) -> pd.DataFrame:
        url = f'{BASE_URL}/exchanges/list'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df

    def get_exchange(self, exchange_id: str) -> pd.DataFrame:
        url = f'{BASE_URL}/exchanges/{exchange_id}'
        response = self.get_response(url)
        df = pd.Series(response).to_frame(name=exchange_id)
        return df

    def get_exchange_tickers(self, exchange_id: str, page:int=1) -> pd.DataFrame:
        """
        100 per page
        """
        url = f'{BASE_URL}/exchanges/{exchange_id}/tickers'
        parameters = {'page': page}
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response['tickers'])
        return df

    def get_exchange_volume(self, exchange_id: str, days: int=7) -> pd.DataFrame:
        url = f'{BASE_URL}/exchanges/{exchange_id}/volume_chart'
        parameters= {'days' : days}
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response).set_index(0)
        df.index = pd.to_datetime(df.index, unit='ms')
        df.rename(columns={1:exchange_id},inplace=True)
        return df

    ## indexes
    def get_index(self) -> str:
        url = f'{BASE_URL}/'
        return 'what is happening here?'

    def get_indexes(self, per_page:int=10, page:int=1) -> pd.DataFrame:
        url = f'{BASE_URL}/indexes'
        parameters = {
                'per_page':per_page,
                'page': page
                }
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response)
        return df

    def get_indexes_list(self) -> pd.DataFrame:
        url = f'{BASE_URL}/indexes/list'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df

    ## derivatives
    def get_derivatives(self) -> pd.DataFrame:
        url = f'{BASE_URL}/derivatives'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df

    def get_derivatives_exchange(self, _id: str) -> pd.DataFrame:
        url = f'{BASE_URL}/derivatives/exchanges/{_id}'
        response = self.get_response(url)
        df = pd.Series(response).to_frame(name=_id)
        return df

    def get_derivatives_exchanges(self, per_page:int=10,page:int=1,order:str=None) -> pd.DataFrame:
        """
        @param order: name_asc，name_desc，open_interest_btc_asc，open_interest_btc_desc，trade_volume_24h_btc_asc，trade_volume_24h_btc_desc
        """
        url = f'{BASE_URL}/derivatives/exchanges/'
        parameters = {
                'per_page':per_page,
                'page': page
                }
        if order:
            parameters['order'] = order

        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response)
        return df

    def get_derivatives_exchanges_list(self) -> pd.DataFrame:
        url = f'{BASE_URL}/derivatives/exchanges/list'
        response = self.get_response(url)
        return pd.DataFrame(response)

    ## Exchange rates
    def get_exchange_rates(self) -> pd.DataFrame:
        url = f'{BASE_URL}/exchange_rates'
        response = self.get_response(url)
        df = pd.Series(response['rates']).to_frame(name='rates')
        return df

    ## Global
    def get_global(self) -> pd.DataFrame:
        url = f'{BASE_URL}/global'
        response = self.get_response(url)
        df = pd.Series(response['data']).to_frame(name='global')
        return df

    def get_global_history(self) -> pd.DataFrame:
        # Ref: https://www.coingecko.com/en/global_charts
        url = 'https://www.coingecko.com/market_cap/total_charts_data?locale=en&vs_currency=usd'
        response = self.get_response(url,headers=HEADERS)
        df = pd.DataFrame(response['stats']).set_index(0)
        df.rename(columns={1:'mktcap.usd'},inplace=True)
        df.index = pd.to_datetime(df.index, unit='ms')
        df.index = df.index.date
        return df

    def get_global_defi(self) -> pd.DataFrame:
        url = f'{BASE_URL}/global/decentralized_finance_defi'
        response = self.get_response(url)
        df = pd.Series(response['data']).to_frame(name='global_defi')
        return df

    ## Companies (beta)
    def get_companies(self, coin_id: str='bitcoin') -> pd.DataFrame:
        """
        Get public companies bitcoin or ethereum holdings (Ordered by total holdings descending)
        @param coin_id: ('bitcoin' or 'ethereum')
        @return: DataFrame 
        """

        url = f'{BASE_URL}/companies/public_treasury/{coin_id}'
        response = self.get_response(url)
        return pd.DataFrame(response['companies'])
