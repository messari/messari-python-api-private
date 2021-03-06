"""This module is meant to contain the SnowTrace class"""

from typing import Union, List
from messari.blockexplorers import Scanner

BASE_URL='https://api.snowtrace.io/api'
class SnowTrace(Scanner):
    """This class is a wrapper around the SnowTrace API
    """

    def __init__(self, api_key: str=None):
        Scanner.__init__(self, base_url=BASE_URL, api_key=api_key)

    ##### Accounts
    # NOTE: no changes

    ##### Contracts
    # NOTE: no changes

    ##### Transactions
    def get_contract_execution_status(self, transactions_in: Union[str, List]) -> None:
        """Override: return None
        """
        return None

    ##### Blocks
    # NOTE: no changes

    ##### Logs
    # NOTE: no changes

    ##### Geth/Parity Proxy
    def get_eth_uncle(self, block: int, index: int):
        """Override: return None
        """
        return None

    ##### Tokens
    # NOTE: no changes

    ##### Gas Tracker
    def get_est_confirmation(self, gas_price: int) -> None:
        """Override: return None
        """
        return None

    def get_gas_oracle(self) -> None:
        """Override: return None
        """
        return None

    ##### Stats

    # TODO, I have convinced myself through testing this is busted on SnowTrace's end
    # Check in on this later

    #def get_total_avax_supply(self) -> int:
    #    """Returns the current amount of Matic (Wei) in circulation.
    #    """
    #    params = {'module': 'stats',
    #              'action': 'AVAXsupply'}
    #    params.update(self.api_dict)
    #    response = self.get_response(self.base_url, params=params)['result']
    #    return int(response)
