# Messari API
Messari provides a free API for crypto prices, market data metrics, on-chain metrics, and qualitative information (asset profiles).

This documentation will provide the basic steps to start using messari’s python library.

This repo is the private repo for internal use at Messari.
Features in the library may or may not be 100% ready for release to the public but they can be useful internally.

For any bugs, feature//integration requests, or asssistance reach out to:
Roberto Talamas or Michael Kremer on slack.

---
### Integrations
* Messari API
* DeFi Llama API
* Token Terminal API
* Deep DAO API
* EVM Block Explorers APIs: Etherscan, Polygonscan, Arbiscan, FTMscan, BSCscan, & SnowTrace
* Solscan API
* Upshot API
* NonFungible API
* OpenSea API
* NFT Floor Price API
* EVM Live Event Monitoring
* FRED API

---
### Remote Install
To install the messari package remotely run this inside of any unix terminal:

```
$> pip install git+https://github.com/messari/messari-python-api-private.git
```


---
### Local Install
To install the messari package from the source:
```
$> git clone https://github.com/messari/messari-python-api-private.git
$> cd messari-python-api-private
messari-python-api-private$> python -m pip install -r requirements.txt
messari-python-api-private$> python setup.py install
```

---
### Quickstart
For a quick demo, you can try the following:
```
$> python
# Import Messari API wrapper
from messari.messari import Messari

# Set up Messari instance
MESSARI_API_KEY = 'add_your_api_key'
messari = Messari(api_key=MESSARI_API_KEY)

# Run a quick demo
markets_df = messari.get_all_markets()
markets_df.head()
```

---
### Docs
To open the offical docs go [here](https://zen-villani-1ab617.netlify.app/).

Examples can be found in [this](https://github.com/messari/messari-python-api-private/blob/master/examples/Messari%20API%20Tutorial.ipynb) Jupyter Notebook. 
