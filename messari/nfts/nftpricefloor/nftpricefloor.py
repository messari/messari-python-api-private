"""This module is meant to contain the NFTPriceFloor class"""

from messari.dataloader import DataLoader
from messari.utils import validate_input
import pandas as pd
from string import Template
from typing import Union, List

NFTS_URL = 'https://api-bff.nftpricefloor.com/nfts'
COLLECTION_URL = Template('https://api-bff.nftpricefloor.com/nft/$collection/chart/pricefloor')
COLLECTION_PARAMS = {'interval':'all'}

HEADERS = {
        'Content-Type': 'application/json',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36',
        }

class NFTPriceFloor(DataLoader):
    """This class is a wrapper around the NFTPriceFloor API
    """
    def __init__(self):
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)

    def get_nfts(self) -> pd.DataFrame:
        """Retrieve basic info for all nfts

        Returns
        -------
            DataFrame
                DataFrame with info on all nfts
        """
        response = self.get_response(NFTS_URL,headers=HEADERS)
        return pd.DataFrame(response)

    def get_floor(self, collection_in: Union[str, List]) -> pd.DataFrame:
        """Retrive floor data for collection(s)

        Parameters
        ----------
            collections_in: str, List
                single collection name in or list of collection names 

        Returns
        -------
            DataFrame
                DataFrame with timeseries price floor
        """
        collections = validate_input(collection_in)
        df_list = []
        for collection in collections:
            endpoint_url = COLLECTION_URL.substitute(collection=collection)
            response = self.get_response(endpoint_url, params=COLLECTION_PARAMS, headers=HEADERS)
            tmp_df = pd.DataFrame(response)
            tmp_df.set_index('dates', inplace=True)
            df_list.append(tmp_df)
        floor_df = pd.concat(df_list, keys=collections, axis=1)
        return floor_df
