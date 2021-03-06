from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name='messari',
    version='0.0.1',
    packages=['messari',
              'messari.coingecko',
              'messari.coinglass',
              'messari.defillama',
              'messari.fred',
              'messari.messari',
              'messari.metabase',
              'messari.tokenterminal',
              'messari.deepdao',
              'messari.eventmonitor',
              'messari.gokustats',
              'messari.nfts',
              'messari.nfts.upshot',
              'messari.nfts.nftpricefloor',
              'messari.nfts.nonfungible',
              'messari.nfts.opensea',
              'messari.blockexplorers',
              'messari.blockexplorers.arbiscan',
              'messari.blockexplorers.bscscan',
              'messari.blockexplorers.etherscan',
              'messari.blockexplorers.ftmscan',
              'messari.blockexplorers.optimisticetherscan',
              'messari.blockexplorers.polygonscan',
              'messari.blockexplorers.snowtrace',
              'messari.blockexplorers.solscan'],
    url='',
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_data={'messari': ['mappings/messari_to_dl.json', 'mappings/messari_to_tt.json']},
    license='MIT`',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    author='Roberto Talamas, Michael Kremer',
    author_email='roberto.talamas@gmail.com, kremeremichael@gmail.com',
    description='Messari API'
)
