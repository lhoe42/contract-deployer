# contract-deployer
Simple script for one click deploying Solidity contracts to either local or remote blockchains

This script compiles a solidity contract and deploys it to a specified provider using a specific account
Usage: python deploycontract.py -c <contract.sol> [-p <provider:port>][-a <account>]

Required libraries: py-solc, web3

Dependency:
`py-solc` requires `solc` to be installed

More information on installing `solc` here: [solc installation documentation](https://solidity.readthedocs.io/en/latest/installing-solidity.html)
