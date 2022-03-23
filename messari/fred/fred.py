"""This module is meant to contain the FRED class"""

from string import Template
from typing import Union, List, Dict
import pandas as pd
import numpy as np

from messari.dataloader import DataLoader
from messari.utils import validate_input, convert_flatten, unpack_list_of_dicts


BASE_URL = 'https://api.stlouisfed.org/fred'

#### Category URLs
category_url = f'{BASE_URL}/category'
category_children_url = f'{BASE_URL}/category/children'
category_related_url = f'{BASE_URL}/category/related'
category_series_url = f'{BASE_URL}/category/series'
category_tags_url = f'{BASE_URL}/category/tags'
category_related_tags_url = f'{BASE_URL}/category/related_tags'

#### Releases URLs
releases_url = f'{BASE_URL}/releases'
releases_dates_url = f'{BASE_URL}/releases/dates'
release_url = f'{BASE_URL}/release'
release_date_url = f'{BASE_URL}/release/dates'
release_series_url = f'{BASE_URL}/release/series'
release_sources_url = f'{BASE_URL}/release/sources'
release_tags_url = f'{BASE_URL}/release/tags'
release_related_tags_url = f'{BASE_URL}/release/related_tags'
release_tables_url = f'{BASE_URL}/release/tables'

#### Series URLs
series_url = f'{BASE_URL}/series'
series_categories_url = f'{BASE_URL}/series/categories'
series_observations_url = f'{BASE_URL}/series/observations'
series_release_url = f'{BASE_URL}/series/release'
series_tags_url = f'{BASE_URL}/series/tags'
series_updates_url = f'{BASE_URL}/series/updates'
series_vintagedates_url = f'{BASE_URL}/series/vintagedates'

#### Sources URLs
sources_url =  f'{BASE_URL}/sources'
source_url =  f'{BASE_URL}/source'
source_releases_url =  f'{BASE_URL}/source/releases'

#### Tags URLs
tags_url = f'{BASE_URL}/tags'
related_tags_url = f'{BASE_URL}/related_tags'
tags_series_url = f'{BASE_URL}/tags/series'

# Get api key: https://fredaccount.stlouisfed.org/apikeys
# docs https://fred.stlouisfed.org/docs/api/fred/

json_dict = {'file_type':'json'}

class FRED(DataLoader):
    """This class is a wrapper around the FRED API
    """
    def __init__(self, api_key=None):
        fred_api_key = {'api_key': api_key}
        DataLoader.__init__(self, api_dict=fred_api_key, taxonomy_dict=None)

    #######################
    # Categories
    #######################
    def get_category(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get a category"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        categories_list = []
        for _id in ids:
            parameters['category_id'] = _id
            response = self.get_response(category_url, params=parameters)
            categories_list.append(response['categories'][0])
        
        return pd.DataFrame(categories_list)

    def get_category_children(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the child categories for a specified parent category"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['category_id'] = _id
            response = self.get_response(category_children_url, params=parameters)
            tmp_df = pd.DataFrame(response['categories'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_category_related(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the related categories for a category"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['category_id'] = _id
            response = self.get_response(category_related_url, params=parameters)
            tmp_df = pd.DataFrame(response['categories'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_category_series(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the series in a category"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['category_id'] = _id
            response = self.get_response(category_series_url, params=parameters)
            tmp_df = pd.DataFrame(response['seriess'])
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
        
    def get_category_tags(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the tags for a category"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['category_id'] = _id
            response = self.get_response(category_tags_url, params=parameters)
            tmp_df = pd.DataFrame(response['tags'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_category_related_tags(self, ids_in: Union[str,List], tags_in: Union[str,List]) -> pd.DataFrame:
        """Get the related tags for a category"""
        parameters = self.api_dict
        parameters.update(json_dict)
        
        tags = validate_input(tags_in)
        tags_joint = ';'.join(tags)
        parameters['tag_names'] = tags_joint

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['category_id'] = _id
            response = self.get_response(category_related_tags_url, params=parameters)
            tmp_df = pd.DataFrame(response['tags'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)

    #######################
    # Releases
    #######################
    def get_releases(self) -> pd.DataFrame:
        """Get all releases of economic data"""
        tmp_list = []
        offset = 0

        parameters = self.api_dict
        parameters.update(json_dict)

        response = self.get_response(releases_url, params=parameters)
        tmp_list += response['releases']
        limit = response['limit']

        while len(response['releases']) == limit:
            offset += limit
            parameters['offset'] = offset
            response = self.get_response(sources_url, params=parameters)
            tmp_list += response['releases']

        releases_df = pd.DataFrame(tmp_list)
        releases_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
        return releases_df
    
    def get_releases_dates(self) -> pd.DataFrame:
        """Get release dates for all releases of economic data"""
        tmp_list = []
        offset = 0

        parameters = self.api_dict
        parameters.update(json_dict)

        response = self.get_response(releases_url, params=parameters)
        tmp_list += response['releases']
        limit = response['limit']

        while len(response['releases']) == limit:
            offset += limit
            parameters['offset'] = offset
            response = self.get_response(releases_dates_url, params=parameters)
            tmp_list += response['releases']
            
        releases_df = pd.DataFrame(tmp_list)
        #releases_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
        return releases_df

    def get_release(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get a release of economic data"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['release_id'] = _id
            response = self.get_response(release_url, params=parameters)
            tmp_df = pd.DataFrame(response['releases'])
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_release_dates(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get release dates for a release of economic data"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['release_id'] = _id
            response = self.get_response(release_date_url, params=parameters)
            tmp_df = pd.DataFrame(response['release_dates'])
            #tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_release_series(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the series on a release of economic data"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['release_id'] = _id
            response = self.get_response(release_series_url, params=parameters)
            tmp_df = pd.DataFrame(response['seriess'])
            #tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_release_sources(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the sources for a release of economic data"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['release_id'] = _id
            response = self.get_response(release_sources_url, params=parameters)
            tmp_df = pd.DataFrame(response['sources'])
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_release_tags(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the tags for a release"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['release_id'] = _id
            response = self.get_response(release_tags_url, params=parameters)
            tmp_df = pd.DataFrame(response['tags'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_release_related_tags(self, ids_in: Union[str,List], tags_in: Union[str,List]) -> pd.DataFrame:
        """Get the related tags for a release"""        
        parameters = self.api_dict
        parameters.update(json_dict)
        
        tags = validate_input(tags_in)
        tags_joint = ';'.join(tags)
        parameters['tag_names'] = tags_joint

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['release_id'] = _id
            response = self.get_response(release_related_tags_url, params=parameters)
            tmp_df = pd.DataFrame(response['tags'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)

    #######################
    # Series
    #######################
    def get_series(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get an economic data series"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['series_id'] = _id
            response = self.get_response(series_url, params=parameters)
            tmp_df = pd.DataFrame(response['seriess'])
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_series_categories(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the categories for an economic data series"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['series_id'] = _id
            response = self.get_response(series_categories_url, params=parameters)
            tmp_df = pd.DataFrame(response['categories'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_series_observations(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the observations or data values for an economic data series"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['series_id'] = _id
            response = self.get_response(series_observations_url, params=parameters)
            tmp_df = pd.DataFrame(response['observations'])
            tmp_df.set_index('date', inplace=True)
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            tmp_df.index = pd.to_datetime(tmp_df.index, format='%Y-%m-%d', errors='coerce')

            df_list.append(tmp_df)
            
        observations_df = pd.concat(df_list, keys=ids, axis=1).xs('value',axis=1, level=1)
        observations_df.replace('.', np.nan, inplace=True)
        return observations_df
    
    def get_series_release(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the release for an economic data series"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['series_id'] = _id
            response = self.get_response(series_release_url, params=parameters)
            tmp_df = pd.DataFrame(response['releases'])
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_series_tags(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the tags for an economic data series"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        df_list = []
        for _id in ids:
            parameters['series_id'] = _id
            response = self.get_response(series_tags_url, params=parameters)
            tmp_df = pd.DataFrame(response['tags'])
            df_list.append(tmp_df)
        
        return pd.concat(df_list, keys=ids, axis=1)
    
    def get_series_updates(self, start_date: str=None, end_date: str=None) -> pd.DataFrame:
        """Get economic data series sorted by when observations were updated on the FRED server
        date format 'YYYY-MM-dd'
        """
        series_updates_url = f'{BASE_URL}/series/updates'

        parameters = self.api_dict
        parameters.update(json_dict)
        
        if start_date:
            parameters['realtime_start'] = start_date
        if end_date:
            parameters['realtime_end'] = end_date

        response = self.get_response(series_updates_url, params=parameters)
        
        return pd.DataFrame(response['seriess'])
    
    def get_series_vintagedates(self, ids_in: Union[str,List]) -> pd.DataFrame:
        """Get the dates in history when a series' data values were revised or new data values were released"""
        parameters = self.api_dict
        parameters.update(json_dict)

        ids = validate_input(ids_in)

        series_list = []
        for _id in ids:
            parameters['series_id'] = _id
            response = self.get_response(series_vintagedates_url, params=parameters)
            
            tmp_series = pd.Series(response['vintage_dates'])
            series_list.append(tmp_series)
        
        return pd.concat(series_list, keys=ids, axis=1)
    
    #######################
    # Sources
    #######################
    def get_sources(self) -> pd.DataFrame:
        """Get all sources of economic data"""
        tmp_list = []
        offset = 0

        parameters = self.api_dict
        parameters.update(json_dict)

        response = self.get_response(sources_url, params=parameters)
        tmp_list += response['sources']
        limit = response['limit']

        while len(response['sources']) == limit:
            offset += limit
            parameters['offset'] = offset
            response = self.get_response(sources_url, params=parameters)
            tmp_list += response['sources']

        sources_df = pd.DataFrame(tmp_list)
        sources_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
        return sources_df
    
    def get_source(self, sources_in: Union[List, str]) -> pd.DataFrame:
        """Get a source of economic data"""
        parameters = self.api_dict
        parameters.update(json_dict)

        sources = validate_input(sources_in)
        
        df_list = []
        for source in sources:
            parameters['source_id'] = source
            response = self.get_response(source_url, params=parameters)
            tmp_df = pd.DataFrame(response['sources'])
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        sources_df = pd.concat(df_list, keys=sources, axis=1)
        return sources_df
    
    def get_source_releases(self, sources_in: Union[List, str]) -> pd.DataFrame:
        """Get the releases for a source"""
        parameters = self.api_dict
        parameters.update(json_dict)

        sources = validate_input(sources_in)
        
        df_list = []
        for source in sources:
            parameters['source_id'] = source
            response = self.get_response(source_releases_url, params=parameters)
            tmp_df = pd.DataFrame(response['releases'])
            tmp_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
            df_list.append(tmp_df)
        
        sources_df = pd.concat(df_list, keys=sources, axis=1)
        return sources_df

    #######################
    # Tags
    #######################
    def get_tags(self) -> pd.DataFrame:
        """Get all tags, search for tags, or get tags by name"""
        tmp_list = []
        offset = 0

        parameters = self.api_dict
        parameters.update(json_dict)

        response = self.get_response(tags_url, params=parameters)
        tmp_list += response['tags']
        limit = response['limit']


        while len(response['tags']) == limit:
            offset += limit
            parameters['offset'] = offset
            response = self.get_response(tags_url, params=parameters)
            tmp_list += response['tags']

        return pd.DataFrame(tmp_list)
    
    def get_related_tags(self, tags_in: Union[List, str]) -> pd.DataFrame:
        """Get the related tags for one or more tags"""
        
        parameters = self.api_dict
        parameters.update(json_dict)

        tags = validate_input(tags_in)
        tags_joint = ';'.join(tags)

        parameters['tag_names'] = tags_joint
        response = self.get_response(related_tags_url, params=parameters)
        
        return pd.DataFrame(response['tags'])
    
    def get_tags_series(self, tags_in: Union[List, str]) -> pd.DataFrame:
        """Get the series matching tags"""
        
        parameters = self.api_dict
        parameters.update(json_dict)

        tags = validate_input(tags_in)
        tags_joint = ';'.join(tags)

        parameters['tag_names'] = tags_joint
        response = self.get_response(tags_series_url, params=parameters)
        
        tags_df = pd.DataFrame(response['seriess'])
        tags_df.drop(['realtime_end', 'realtime_start'], axis=1, inplace=True)
        return tags_df
