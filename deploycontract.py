# Contract Deployment Tool
# Veriteos, Inc. 2018
# 
# This script compiles a solidity contract and deploys it to a specified provider using a specific account
#
# Usage: python deploycontract.py -c <contract.sol> [-p <provider:port>][-a <account>]

import sys
import web3
import argparse

from web3 import Web3
from solc import compile_source

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--contract", required=True,
	help="filename of smart contract")
ap.add_argument("-p", "--provider", required=False,
	help='RPC provider endpoint address (default is localhost port 8545)')
ap.add_argument("-a", "--account", required=False,
	help="Deployment account address (defaults to first account in eth.accounts)")
args = vars(ap.parse_args())

# assign contract name
contract_name = args["contract"]

# assign provider name (defaults to http://127.0.0.1:8545)
if args["provider"] is not None:
    provider = args["provider"]
else:
    provider = "http://127.0.0.1:8545"

# instantiate provider - default method for Veriteo is HTTP
w3 = Web3(Web3.HTTPProvider(provider))

# Use the first test account in the client if not specified
if args["account"] is not None:
    w3.eth.accounts = args["account"]
else:
    w3.eth.defaultAccount = w3.eth.accounts[0]

# helper function to read and compile 
def compile_source_file(file_path):
   with open(file_path, 'r') as f:
      source = f.read()
   return compile_source(source)

def gasCost(keyhash):
    return w3.eth.getTransactionReceipt(keyhash)['gasUsed']

def showGasCost(tx_hash):
    print('This transaction cost',gasCost(tx_hash),'gas.')

def deploy_contract(w3, contract_interface):
    # deploys a contract and returns contract address
    Contract = w3.eth.contract(abi=contract_interface['abi'],bytecode=contract_interface['bin'])
    tx_hash = Contract.constructor().transact()
    address = w3.eth.getTransactionReceipt(tx_hash)['contractAddress']
   
    return address,tx_hash

def initDeployContract(contract_name):
    # this module reads the smart contract, compiles, deploys and instantiates. Returns the contract
    # as a concise contract

    # compile from command line argument
    compiled_sol = compile_source_file(contract_name)
    
    # separate KV pair of id and interface
    contract_id, contract_interface = compiled_sol.popitem()
    
    # deploy contract to w3 
    contract_address,tx_hash = deploy_contract(w3, contract_interface)

    print("\nDeployed contract {0} to address: {1}".format(contract_id, contract_address))
    showGasCost(tx_hash)

    # instantiate the deployed contract named contract
    contract = w3.eth.contract(address=contract_address, abi= contract_interface['abi'],)
    
    return contract

def instantiateContract(contract_name,contract_address):
    # Instantiate a contract that already is deployed. Requires original contract in order to generate ABI

    # compile from command line argument
    compiled_sol = compile_source_file(contract_name)
    
    # separate KV pair of id and interface
    contract_id, contract_interface = compiled_sol.popitem()
    
    # instantiate the deployed contract named contract
    contract = w3.eth.contract(address=contract_address, abi= contract_interface['abi'],)
    
    return contract

# Instantiate the contract
def main():
    contract = initDeployContract(contract_name)
    print('\nContract',contract_name,'successfully deployed.\n')

if __name__ == "__main__":
    main()