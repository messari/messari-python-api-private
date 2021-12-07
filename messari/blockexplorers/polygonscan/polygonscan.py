"""This module is meant to contain the Polygonscan class"""


from messari.blockexplorers import Scanner

BASE_URL='https://api.polygonscan.io/api'
class Polygonscan(Scanner):
    """This class is a wrapper around the Polygonscan API
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
    # NOTE: no changes

    ##### Tokens
    def get_token_circulating_supply(self, tokens_in: Union[str, List]) -> pd.DataFrame:
        """Returns ERC20-Token Circulating Supply (Applicable for Polygon Cross Chain token Types) by ContractAddress
        """
        tokens = validate_input(tokens_in)
        supply_dict = {}
        for token in tokens:
            params = {'module': 'stats',
                      'action': 'tokenCsupply',
                      'contractaddress': token}
            params.update(self.api_dict)
            supply = self.get_response(self.BASE_URL, params=params)['result']
            supply_dict[token] = supply
        supply_df = pd.Series(supply_dict).to_frame(name='supply')
        return supply_df
    ##### Gas Tracker
    def get_est_confirmation(self, gas_price: int) -> None:
        """Override: return None
        """
        return None

    def get_gas_oracle(self) -> None:
        """Override: return None
        """
        return None