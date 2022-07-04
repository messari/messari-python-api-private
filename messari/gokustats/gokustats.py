"""This module is meant to contain the GokuStats class"""

import requests
import pandas as pd

from messari.dataloader import DataLoader

class GokuStats(DataLoader):
    """
    This class is a wrapper around GokuStats
    Reference: https://www.gokustats.xyz/dashboard
    """
    def __init__(self):
        DataLoader.__init__(self,api_dict=None,taxonomy_dict=None)
        
    ### General ###
    def get_datatable(self) -> pd.DataFrame:
        url = 'https://api.gokustats.xyz/datatable/'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df
    
    ### Fundamentals ###
    def get_daily_active_addresses(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-active-addresses/'
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response)
        return df
    
    def get_daily_transactions(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-transactions/'
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df
    
    def get_daily_tvl(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-total-value-locked/'
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df
    
    ### Stablecoins ###
    def get_daily_stablecoin_market_cap(self, days_back: int=1095) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
        }
        url = 'https://api.gokustats.xyz/daily-stablecoin-market-caps/'
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df
        
    def get_cumulative_stablecoin_market_cap(self, days_back: int=1095) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
        }
        url = 'https://api.gokustats.xyz/cumulative-stablecoin-market-caps/'
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df
    
    ### Social ###
    def get_daily_twitter_followers(self, days_back: int=1095) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
        }
        url = 'https://api.gokustats.xyz/daily-twitter-followers/'
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df
        
    def get_cumulative_twitter_followers(self, days_back: int=1095) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
        }
        url = 'https://api.gokustats.xyz/cumulative-twitter-followers/'
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df
    
    ### Market Data ###
    def get_daily_prices(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-prices/'
        response = self.get_response(url,params=parameters)
        df = pd.DataFrame(response)
        return df
    
    def get_daily_market_caps(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-market-caps/'
        response = self.get_response(url, params=parameters)
        df = pd.DataFrame(response)
        return df
    
    ### Valuation ###
    def get_daily_market_cap_over_active_addresses(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-market-cap-over-active-addresses/'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df
    
    def get_daily_market_cap_over_transactions(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-market-cap-over-transactions/'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df
    
    def get_daily_market_cap_over_tvl(self, days_back: int=1095, percent_change: bool=False) -> pd.DataFrame:
        parameters = {
            'daysBack': days_back,
            'percentChange': percent_change,
            'baseCurrency': 'USD'
        }
        url = 'https://api.gokustats.xyz/daily-market-cap-over-tvl/'
        response = self.get_response(url)
        df = pd.DataFrame(response)
        return df
