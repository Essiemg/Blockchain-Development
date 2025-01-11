import streamlit as st
from web3 import Web3
import time


class SmartContracts:
    def __init__(self, provider_url: str):
        """Initialize Web3 and check connection to Ethereum."""
        self.w3 = Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/a53f296d4f5847f3b514612eb52ba3cb"))
        if not self.w3.is_connected():
            st.error("Failed to connect to the Ethereum network.")
            raise ConnectionError("Could not connect to the blockchain.")
        else:
            st.success("Connected to the Ethereum network.")

    def get_contract(self, address, abi):

        address = Web3.to_checksum_address(address)
        #Return a contract instance.
        return self.w3.eth.contract(address=address, abi=abi)

    # Contract Functions
    def stake_tokens(self, amount, user_address):
        tx_hash = self.gamify_contract.functions.stakeTokens().transact( {
            'from': user_address,
            'value': self.w3.toWei(amount, 'ether'),
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def claim_rewards(self, user_address):
        tx_hash = self.gamify_contractfunctions.claimReward().transact({
            'from': user_address,
            'gas': 2000000,
            'gasPrice': self.w3.toWei('50', 'gwei')
        })
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def get_leaderboard(self):
        return self.leaderboard_contract.functions.getTopPlayers().call()

    def transfer_energy_tokens(self, to_address, amount, user_address):
        tx_hash = self.energy_token_contract.functions.transfer(
            to_address, amount
        ).transact({'from': user_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def list_item(self, item_id, price, user_address):
        tx_hash = self.marketplace_contract.functions.addItem(
            item_id, price, 1  # Assume stock = 1
        ).transact({'': user_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash

    def buy_item(self, item_id, user_address):
        tx_hash = self.marketplace_contract.functions.buyItem(
            item_id, 1  # Assume quantity = 1
        ).transact({'from': user_address})
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_hash


# Streamlit App UI
st.title("Smart Grid Guardians")

# Initialize the SmartContracts class
provider_url = "https://mainnet.infura.io/v3/a53f296d4f5847f3b514612eb52ba3cb"
smart_contracts = SmartContracts(provider_url)

# Set up example contract ABIs and addresses
gamify_abi = [
    {
        "inputs": [{"internalType": "address", "name": "_player", "type": "address"},
                   {"internalType": "uint256", "name": "_score", "type": "uint256"}],
        "name": "achieveGoal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "claimReward",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
gamify_address = "0x63ece6ba0e52d57828d7e1dbf3c4490f854adaa9"
gamify_address_checksum = Web3.to_checksum_address(gamify_address)
smart_contracts_gamify_contract = smart_contracts.get_contract(gamify_address_checksum, gamify_abi)

leaderboard_abi = [
    {
        "inputs": [],
        "name": "getTopPlayers",
        "outputs": [
            {
                "components": [
                    {"internalType": "address", "name": "playerAddress", "type": "address"},
                    {"internalType": "uint256", "name": "score", "type": "uint256"}
                ],
                "internalType": "struct Leaderboard.Player[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
leaderboard_address = "0xd4ecbf286e01597671f3e105ff8d62ff169b64e7"
leaderboard_address_checksum = Web3.to_checksum_address(leaderboard_address)

smart_contracts_leaderboard_contract = smart_contracts.get_contract(leaderboard_address_checksum, leaderboard_abi)

energy_token_abi = [
    {
        "inputs": [{"internalType": "address", "name": "to", "type": "address"},
                   {"internalType": "uint256", "name": "amount", "type": "uint256"}],
        "name": "transfer",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
energy_token_address_checksum = "0x454e9ac208dd339beefc0e5146fca1b18cd155ec"
energy_token_checksum = Web3.to_checksum_address(energy_token_address_checksum)

smart_contracts_energy_token_contract = smart_contracts.get_contract(energy_token_address_checksum, energy_token_abi)

marketplace_abi = [
    {
        "inputs": [{"internalType": "string", "name": "name", "type": "string"},
                   {"internalType": "uint256", "name": "price", "type": "uint256"},
                   {"internalType": "uint256", "name": "stock", "type": "uint256"}],
        "name": "addItem",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
marketplace_address ="0xd9145CCE52D386f254917e481eB44e9943F39138"
marketplace_address_checksum = Web3.to_checksum_address(marketplace_address)

smart_contracts_marketplace_contract = smart_contracts.get_contract(marketplace_address_checksum, marketplace_abi)

# User inputs for interaction
user_address = st.text_input("Your Wallet Address")

if st.button("Stake Tokens"):
    amount = st.number_input("Amount to Stake", min_value=0.0)
    if user_address:
        tx_hash = smart_contracts.stake_tokens(amount, user_address)
        st.success(f"Tokens Staked! Transaction Hash: {tx_hash.hex()}")

if st.button("Get Leaderboard"):
    leaderboard = smart_contracts.get_leaderboard()
    st.write(leaderboard)

if st.button("Transfer Energy Tokens"):
    to_address = st.text_input("Transfer To Address")
    amount = st.number_input("Amount to Transfer", min_value=0)
    if user_address and to_address:
        tx_hash = smart_contracts.transfer_energy_tokens(to_address, amount, user_address)
        st.success(f"Tokens Transferred! Transaction Hash: {tx_hash.hex()}")

if st.button("List Item"):
    item_id = st.text_input("Item ID")
    price = st.number_input("Price", min_value=0)
    if user_address and item_id:
        tx_hash = smart_contracts.list_item(item_id, price, user_address)
        st.success(f"Item Listed! Transaction Hash: {tx_hash.hex()}")

if st.button("Buy Item"):
    item_id = st.text_input("Item ID to Buy")
    if user_address and item_id:
        tx_hash = smart_contracts.buy_item(item_id, user_address)
        st.success(f"Item Bought! Transaction Hash: {tx_hash.hex()}")
