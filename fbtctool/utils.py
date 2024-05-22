from web3 import Web3
from . import config
from .contract import ContractFactory

def get_web3(chain_id: int):
    assert chain_id in config.FBTC_DEPLOYMENT, f"Unknown chain {chain_id}"
    rpc_url = config.FBTC_DEPLOYMENT[chain_id]["rpc"]
    return Web3(Web3.HTTPProvider(rpc_url))

def get_factory(chain_id: int):
    assert chain_id in config.FBTC_DEPLOYMENT, f"Unknown chain {chain_id}"
    rpc = config.FBTC_DEPLOYMENT[chain_id]["rpc"]
    return ContractFactory(rpc)

def get_bridge(chain_id: int, bridge_addr: str = None):
    assert chain_id in config.FBTC_DEPLOYMENT, f"Unknown chain {chain_id}"
    rpc = config.FBTC_DEPLOYMENT[chain_id]["rpc"]
    if bridge_addr is None:
        bridge_addr = config.FBTC_DEPLOYMENT[chain_id]["bridge"]
    return ContractFactory(rpc).contract(bridge_addr, "FireBridge")