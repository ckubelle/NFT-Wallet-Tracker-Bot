import os
import requests
from dotenv import load_dotenv

load_dotenv()


ETHERSCAN_KEY = os.getenv('ETHERSCAN_KEY')
WALLET_ADDRESS = os.getenv('WALLET_ADDRESS')

def getEtherBal():
    ether_bal_response = requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={WALLET_ADDRESS}&tag=latest&apikey={ETHERSCAN_KEY}')

    ether_bal = float(ether_bal_response.json()["result"])

    #Convert from wei to ETH
    ether_bal /= 1000000000000000000

    print("Your wallet address is: ", ether_bal)

if __name__ == "__main__":
    getEtherBal()