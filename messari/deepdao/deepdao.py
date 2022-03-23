"""This module is meant to contain the Deep DAO class"""

import requests
from string import Template
from typing import Union, List
import json
import pandas as pd
import numpy as np

from messari.dataloader import DataLoader
from messari.utils import validate_input
from .helpers import unpack_dataframe_of_lists, unpack_dataframe_of_dicts

##########################
# URL Endpoints
##########################
## DAOs
ORGANIZATIONS_URL = 'https://golden-gate-server.deepdao.io/dashboard/organizations'
DASHBOARD_URL = 'https://golden-gate-server.deepdao.io/dashboard/ksdf3ksa-937slj3'
DAO_URL = Template('https://golden-gate-server.deepdao.io/organization/ksdf3ksa-937slj3/$dao_id')

## People
#PEOPLE_URL = 'https://golden-gate-server.deepdao.io/people/top'
PEOPLE_URL = 'https://golden-gate-server.deepdao.io/people/top'
USER_URL = Template('https://golden-gate-server.deepdao.io/user/2/$user') #user is 0xpubkey
USER_PROPOSALS_URL = Template('https://golden-gate-server.deepdao.io/user/2/$user/proposals')
USER_VOTES_URL = Template('https://golden-gate-server.deepdao.io/user/2/$user/votes')

HEADERS = {
    "accept": "application/json",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36", # pylint: disable=line-too-long
}


#### DAOs
class DeepDAO(DataLoader):
    """This class is a wrapper around the DeepDAO API
    """

    def __init__(self):
        # Need to init DataLoader first to have get_respone work in rest of __init__
        DataLoader.__init__(self, api_dict=None, taxonomy_dict=None)

        people = self.get_top_members(count=100000)
        people_dict={}
        address_dict={}
        # TODO, do this without unused variable 'index'
        for index, person in people.iterrows(): # pylint: disable=unused-variable
            people_dict[person['address']] = person['name']
            address_dict[person['name']] = person['address']

        # get person
        self.people_tax = people_dict
        # get address
        self.address_tax = address_dict

        summary = self.get_summary()
        name_dict={}
        id_dict={}
        for index, dao in summary.iterrows():
            name_dict[dao['organizationId']] = dao['daoName']
            id_dict[dao['daoName']] = dao['organizationId']

        # get name
        self.name_tax = name_dict
        # get id
        self.id_tax = id_dict

    ####### Class helpers
    def get_dao_list(self) -> List:
        """Returns list of DAOs tracked by Deep DAO
        Returns
        -------
           list
               list of DAOs
        """
        return list(self.id_tax.keys())

    def get_member_list(self) -> List:
        """Returns list of DAO members tracked by Deep DAO
        Returns
        -------
           list
               list of memberss
        """
        return list(self.address_tax.keys())



    ####### Overview
    def get_organizations(self) -> pd.DataFrame:
        """Returns basic info for all Deep DAO tracked organizations
        Returns
        -------
           DataFrame
               pandas DataFrame of Deep DAO organizations info
        """
        organizations = requests.get(ORGANIZATIONS_URL, headers=HEADERS).json()
        organizations_df = pd.DataFrame(organizations)
        return organizations_df

    def get_summary(self) -> pd.DataFrame:
        """Returns basic summaries of information for all Deep DAO tracked organizations
        Returns
        -------
           DataFrame
               pandas DataFrame of Deep DAO organizations summaries
        """
        response = requests.get(DASHBOARD_URL, headers=HEADERS).json()
        summary = response['daosSummary']
        summary_df = pd.DataFrame(summary)
        summary_df.drop('daosArr', axis=1, inplace=True, errors='ignore')
        return summary_df

    def get_overview(self) -> pd.DataFrame:
        """Returns an overview of the DAO ecosystem aggreated by Deep DAO
        Returns
        -------
           DataFrame
               pandas DataFrame of DAO ecosystem overview
        """
        response = requests.get(DASHBOARD_URL, headers=HEADERS).json()
        overview = response['daoEcosystemOverview']
        dict_list = []
        count=0
        for date in overview['datesArray']:
            ts_dict = {'date': date,
                       'aum': overview['aumArray'][count],
                       'members': overview['membersArray'][count],
                       'over1M': overview['over1MArray'][count],
                       'over50k': overview['over50KArray'][count],
                       'over10Members': overview['over10MembersArray'][count],
                       'over100Members': overview['over100MembersArray'][count]}
            dict_list.append(ts_dict)
            count+=1
        overview_df = pd.DataFrame(dict_list)
        overview_df.set_index('date', inplace=True)
        old_index = overview_df.index
        new_index = []
        for index in old_index:
            dt_string = str(index).split('T', maxsplit=1)[0]
            new_index.append(dt_string)
        overview_df.index=new_index
        # drop last row because it's not formatted correctly & data is weird
        # TODO look into this
        overview_df.drop(overview_df.tail(1).index,inplace=True)
        overview_df.index = pd.to_datetime(overview_df.index, format='%Y-%m-%d')
        overview_df = overview_df[~overview_df.index.duplicated(keep='last')]
        return overview_df

    def get_rankings(self) -> pd.DataFrame:
        """Returns rankings for organizations tracked by Deep DAO
        Returns
        -------
           DataFrame
               pandas DataFrame of Deep DAO organizations rankings
        """
        response = requests.get(DASHBOARD_URL, headers=HEADERS).json()
        rankings = response['daoEcosystemOverview']['daoRankings']
        rankings_df = pd.DataFrame(rankings)
        rankings_df.drop('date', axis=1, inplace=True)
        return rankings_df

    def get_tokens(self) -> pd.DataFrame:
        """Returns information about the utilization of different tokens
        Returns
        -------
           DataFrame
               pandas DataFrame with token utilization
        """
        response = requests.get(DASHBOARD_URL, headers=HEADERS).json()
        tokens = response['daoTokens']
        tokens_df = pd.DataFrame(tokens)
        return tokens_df


    ####### Overview
    def get_dao_info(self, dao_slugs: Union[str, List]) -> pd.DataFrame:
        """Returns basic information for given DAO(s)
        Parameters
        ----------
            dao_slugs: Union[str, List]
                Input DAO names as a string or list (ex. 'Uniswap')

        Returns
        -------
           DataFrame
               pandas DataFrame with general DAO information
        """

        slugs = validate_input(dao_slugs)

        dao_info_list = []
        for slug in slugs:
            # TODO swap w/ validate
            if slug in self.id_tax:
                dao_id = self.id_tax[slug]
            else:
                dao_id = slug
            endpoint_url = DAO_URL.substitute(dao_id=dao_id)
            dao_info = self.get_response(endpoint_url, headers=HEADERS)['data']
            dao_info_series = pd.Series(dao_info)
            dao_info_list.append(dao_info_series)

        dao_info_df = pd.concat(dao_info_list, keys=slugs, axis=1)
        dao_info_df.drop(['rankings', 'indices', 'proposals', 'members', 'votersCoalition', 'financial'], inplace=True, errors='ignore')
        return dao_info_df

    def get_dao_activity(self, dao_slugs: Union[str, List]) -> pd.DataFrame:
        """Returns basic activity for given DAO(s)
        Parameters
        ----------
            dao_slugs: Union[str, List]
                Input DAO names as a string or list (ex. 'Uniswap')

        Returns
        -------
           DataFrame
               pandas DataFrame with DAO activity
        """
        slugs = validate_input(dao_slugs)
        dao_info_list = []
        for slug in slugs:
            # TODO swap w/ validate
            if slug in self.id_tax:
                dao_id = self.id_tax[slug]
            else:
                dao_id = slug
            endpoint_url = DAO_URL.substitute(dao_id=dao_id) + '/governance/activity'
            dao_info = self.get_response(endpoint_url, headers=HEADERS)['data']['monthlyActivity']
            dao_df = pd.DataFrame(dao_info)
            dao_df.set_index('createdAt', inplace=True)
            dao_df.index = pd.to_datetime(dao_df.index)
            dao_info_list.append(dao_df)
        dao_info_df = pd.concat(dao_info_list, keys=slugs, axis=1)
        return dao_info_df


    def get_dao_proposals(self, dao_slugs: Union[str, List]) -> pd.DataFrame:
        """Returns information about governance proposals for given DAO(s)
        Parameters
        ----------
            dao_slugs: Union[str, List]
                Input DAO names as a string or list (ex. 'Uniswap')

        Returns
        -------
           DataFrame
               pandas DataFrame with DAO governance proposals
        """
        ### TODO extract nested lists & dicts

        slugs = validate_input(dao_slugs)

        dao_info_list = []
        for slug in slugs:
            # TODO swap w/ validate
            if slug in self.id_tax:
                dao_id = self.id_tax[slug]
            else:
                dao_id = slug
            endpoint_url = DAO_URL.substitute(dao_id=dao_id) + '/governance/decisions'
            dao_info = self.get_response(endpoint_url, headers=HEADERS)
            dao_info_series = pd.Series(dao_info)
            dao_info_list.append(dao_info_series)

        dao_info_df = pd.concat(dao_info_list, keys=slugs, axis=1)
        proposals = dao_info_df.loc['decisions']

        proposals_list = []
        for proposal in proposals:
            data = json.loads(proposal)
            data_series = pd.Series(data)
            proposals_list.append(data_series)
        proposals_df = pd.concat(proposals_list, keys=slugs, axis=1)

        proposals_df = unpack_dataframe_of_dicts(proposals_df)


        return proposals_df

    def get_dao_members(self, dao_slugs: Union[str, List]) -> pd.DataFrame:
        """Returns information about the Members of given DAO(s)
        Parameters
        ----------
            dao_slugs: Union[str, List]
                Input DAO names as a string or list (ex. 'Uniswap')

        Returns
        -------
           DataFrame
               pandas DataFrame with DAO Members
        """
        ### TODO extract nested lists & dicts

        slugs = validate_input(dao_slugs)

        dao_info_list = []
        for slug in slugs:
            # TODO swap w/ validate
            if slug in self.id_tax:
                dao_id = self.id_tax[slug]
            else:
                dao_id = slug
            endpoint_url = DAO_URL.substitute(dao_id=dao_id) + '/top-shareholders'
            dao_info = self.get_response(endpoint_url, headers=HEADERS)['shareholders']
            dao_info_df = pd.DataFrame(dao_info)
            dao_info_list.append(dao_info_df)

        dao_info_df = pd.concat(dao_info_list, keys=slugs, axis=1)
        return dao_info_df

    def get_dao_voter_coalitions(self, dao_slugs: Union[str, List]) -> pd.DataFrame:
        """Returns information about different voting coalitions for given DAO(s)
        Parameters
        ----------
            dao_slugs: Union[str, List]
                Input DAO names as a string or list (ex. 'Uniswap')

        Returns
        -------
           DataFrame
               pandas DataFrame with DAO voter coalitions
        """
        ### TODO extract nested lists & dicts

        slugs = validate_input(dao_slugs)

        dao_info_list = []
        for slug in slugs:
            # TODO swap w/ validate
            if slug in self.id_tax:
                dao_id = self.id_tax[slug]
            else:
                dao_id = slug
            endpoint_url = DAO_URL.substitute(dao_id=dao_id)
            dao_info = self.get_response(endpoint_url, headers=HEADERS)
            dao_info_series = pd.Series(dao_info)
            dao_info_list.append(dao_info_series)

        dao_info_df = pd.concat(dao_info_list, keys=slugs, axis=1)
        coalitions = dao_info_df.loc['votersCoalition']

        coalitions_list = []
        for coalition in coalitions:
            data = json.loads(coalition)
            data_series = pd.Series(data)
            coalitions_list.append(data_series)

        coalitions_df = pd.concat(coalitions_list, keys=slugs, axis=1)


        coalitions_df = unpack_dataframe_of_lists(coalitions_df)
        # TODO
        #coalitions_df.rename(columns={"subsetLength": "size"}, inplace=True)



        return coalitions_df

    def get_dao_financials(self, dao_slugs: Union[str, List]) -> pd.DataFrame:
        """Returns information about the financials of given DAO(s)
        Parameters
        ----------
            dao_slugs: Union[str, List]
                Input DAO names as a string or list (ex. 'Uniswap')

        Returns
        -------
           DataFrame
               pandas DataFrame with DAO financials
        """
        ### TODO extract nested lists & dicts

        slugs = validate_input(dao_slugs)

        dao_info_list = []
        for slug in slugs:
            # TODO swap w/ validate
            if slug in self.id_tax:
                dao_id = self.id_tax[slug]
            else:
                dao_id = slug
            endpoint_url = DAO_URL.substitute(dao_id=dao_id) + '/currencies'
            dao_info = self.get_response(endpoint_url, headers=HEADERS)['currencies']
            dao_info_series = pd.Series(dao_info)
            dao_info_list.append(dao_info_series)

        dao_info_df = pd.concat(dao_info_list, keys=slugs, axis=1)

        # TODO, should handle this in top loop
        df_list = []
        for slug in slugs:
            sub_df = pd.DataFrame(dao_info_df[slug].dropna().tolist())
            df_list.append(sub_df)
        fin_df = pd.concat(df_list, axis=1, keys=slugs)
        return fin_df

    ####### Members
    def get_top_members(self, count: int=50) -> pd.DataFrame:
        """Returns a dataframe of basic information for the the top Members
        Sorted by amount of DAO's particpating in.

        Parameters
        ----------
            count: int
                Amount of members to return info for (default=50)

        Returns
        -------
           DataFrame
               pandas DataFrame with top members across DAOs
        """
        #TODO can work on paging this
        params = {'limit': count,
                  'offset': 0,
                  'sortBy': 'daoAmount'}
        people = self.get_response(PEOPLE_URL, params=params, headers=HEADERS)
        people_df = pd.DataFrame(people)
        return people_df

    def get_member_info(self, pubkeys: Union[str, List]) -> pd.DataFrame:
        """Returns basic information for given member(s)
        Parameters
        ----------
            pubkeys: Union[str, List]
                Input public keys for DAO members as a string or list

        Returns
        -------
           DataFrame
               pandas DataFrame with member information
        """
        users = validate_input(pubkeys)
        user_info_list = []
        for user in users:
            if user in self.address_tax:
                user_address = self.address_tax[user]
            else:
                user_address = user
            endpoint_url = USER_URL.substitute(user=user_address)
            user_info = requests.get(endpoint_url, headers=HEADERS).json()
            user_info_series = pd.Series(user_info)
            user_info_list.append(user_info_series)
        users_info_df = pd.concat(user_info_list, keys=users, axis=1)
        return users_info_df

    def get_member_votes(self, pubkeys: Union[str, List]) -> pd.DataFrame:
        """Returns voting history for given member(s)
        Parameters
        ----------
            pubkeys: Union[str, List]
                Input public keys for DAO members as a string or list

        Returns
        -------
           DataFrame
               pandas DataFrame with member voting history
        """
        users = validate_input(pubkeys)
        votes_info_list = []
        for user in users:
            if user in self.address_tax:
                user_address = self.address_tax[user]
            else:
                user_address = user
            endpoint_url = USER_VOTES_URL.substitute(user=user_address)
            print(endpoint_url)
            votes_info = self.get_response(endpoint_url, headers=HEADERS)
            votes_info_series = pd.Series(votes_info)
            votes_info_list.append(votes_info_series)

        votes_info_df = pd.concat(votes_info_list, keys=users, axis=1)

        old_index = votes_info_df.index
        new_index = []
        for old in old_index:
            if old in self.name_tax:
                new_index.append(self.name_tax[old])
            else:
                new_index.append(old)
        votes_info_df.index = new_index

        old_columns = votes_info_df.columns
        new_columns = []
        for old in old_columns:
            if old in self.people_tax:
                new_columns.append(self.people_tax[old])
            else:
                new_columns.append(old)
        votes_info_df.columns = new_columns

        votes_df = unpack_dataframe_of_lists(votes_info_df)

        return votes_df
