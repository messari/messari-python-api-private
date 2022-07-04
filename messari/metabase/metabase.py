"""This module is meant to contain the Metabase class"""

import json
import requests
import pandas as pd
from typing import List

# async jazz
import asyncio
from aiohttp import ClientSession

from messari.dataloader import DataLoader

HEADERS = {
    'Content-Type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
}

class Metabase(DataLoader):
    
    def __init__(self, url: str, ignore_list: List[str]=[]):

        # Init DataLoader
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)
        
        # set key values
        self.url = url
        self.ignore_list = ignore_list
        
        # use url to get cards df
        self.cards = self.get_cards()
        
    ###################
    # Cards
    def identify_request_url(self, cards: pd.DataFrame) -> pd.DataFrame:
        """
        Test the two possible formats for the request url, and insert the correct url into the dataframe
        """
        test_card_id = int(cards.at[0, 'card_id'])
        test_dashboard_id = cards.at[0, 'dashboard']

        test_request_url = f'{test_dashboard_id}/card/{test_card_id}'
        response = requests.get(test_request_url, headers=HEADERS, timeout=60)

        # if there is a response from the call, then use the first format
        # TODO: use 'if not response' and remove the else statement
        if response:
            print('Utilizing url format: /dashboard id/card/card id')
            for idx, row in cards.iterrows():
                card_id = int(row['card_id'])
                dashboard = row['dashboard']
                cards.at[idx, 'request_url'] = f'{dashboard}/card/{card_id}'

        # use second format if first format did not return a response
        else:
            # print('Utilizing url format: /dashboard id/dashcard id/card/card id')
            for idx, row in cards.iterrows():
                card_id = int(row['card_id'])
                dashcard_id = int(row['dashcard_id'])
                dashboard = row['dashboard']
                cards.at[idx, 'request_url'] = f'{dashboard}/dashcard/{dashcard_id}/card/{card_id}'

        return cards
    
    def get_cards(self) -> pd.DataFrame:
        #url = 'https://dashboard.chaincrunch.cc/api/public/dashboard/873471ae-497e-49f7-99aa-9c2e8e62c58d'
        response = requests.get(self.url, headers=HEADERS).json()
        cards = pd.DataFrame(response['ordered_cards'])

        dashcard_ids = cards['id']
        card_ids = cards['card_id']

        cards = pd.DataFrame(cards['card'].tolist())
        cards.drop(labels=['id', 'visualization_settings', 'dataset_query'], axis=1, inplace=True, errors='ignore')

        cards['card_id'] = card_ids
        cards['dashcard_id'] = dashcard_ids
        cards['dashboard'] = self.url

        # Drop cards in ignore list
        cards = cards[~cards['name'].isin(self.ignore_list)]

        # Drop any null card ids
        cards = cards[~pd.isnull(cards['card_id'])] #card_id

        # reset index after dropping rows
        cards.reset_index(inplace=True)
        cards.drop(labels='index', axis=1, inplace=True, errors='ignore')
        cards = self.identify_request_url(cards)
        return cards
    
    ###############
    # running urls
    async def run_url(self, url: str, session, name: str) -> pd.DataFrame:
        print(name, url)
        try:
            response = await session.get(url,headers=HEADERS,timeout=60)
        except asyncio.TimeoutError as err:
            print(name, url, err)
            return pd.DataFrame()
        response = await response.json()

        # Rare case response is empty
        if 'data' not in response:
            print(name, url, 'empty response')
            df = pd.DataFrame()
            df.name = name
            df.url = url
            return df

        df = pd.DataFrame(response['data']['rows'])

        if df.empty:
            print(url, name, 'empty df')
            df.name = name
            df.url = url
            return df

        # TODO: Handle timeseries data
        cols_df = pd.DataFrame(response['data']['cols'])
        df.columns = cols_df['name'].tolist()
        df.name = name
        df.url = url
        return df

    async def run(self) -> List[pd.DataFrame]:
        
        # Unpack cards into urls & names to query
        urls = list(
            zip(
                self.cards['request_url'].tolist(),
                self.cards['name'].tolist()
            )
        )

        # Query urls & names
        async with ClientSession() as session:
            # results = [(card dataframe, card name), (card dataframe, card name), ...]
            results = await asyncio.gather(*[self.run_url(item[0], session, item[1]) for item in urls])

        # TODO, find a way to organize these results
        self.results = results
        return             
