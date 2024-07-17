import sys

from web3 import Web3

from . import config
from .contract import ContractFactory


def get_btc_rpc(url_or_name: str):
    for k, v in config.BTC_RPC.items():
        if k == url_or_name.lower():
            return v
    return url_or_name


def get_evm_rpc(url_or_name: str):
    for cfg in config.FBTC_DEPLOYMENT.values():
        if cfg["name"] == url_or_name.lower():
            return cfg["rpc"]
    return url_or_name


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


def read_json() -> str:
    cnt = 0
    s = ""
    while True:
        c = sys.stdin.read(1)
        s += c
        if c == "{":
            cnt += 1
        elif c == "}":
            cnt -= 1
            if cnt == 0:
                return s


class Printer(object):
    def __init__(self) -> None:
        self._indent_cnt = 0

    def print(self, *args, **kwargs):
        indent = " " * self._indent_cnt
        print(indent, *args, **kwargs)

    def line(self, size=80, c="="):
        self.print(c * size)

    def indent(self, size=4):
        _printer = self

        class _Indent(object):
            def __enter__(self):
                nonlocal _printer
                nonlocal size
                _printer._indent_cnt += size

            def __exit__(self, *args):
                nonlocal _printer
                nonlocal size
                _printer._indent_cnt -= size

        return _Indent()


EVM_CHAIN_ID_TO_NAME = {
    1: "Ethereum Mainnet",
    56: "BNB Smart Chain",
    11155111: "Ethereum Sepolia Testnet",
    5000: "Mantle",
    5003: "Mantle Sepolia Testnet",
}

FBTC_CHAIN_ID_TO_NAME = {
    "0100000000000000000000000000000000000000000000000000000000000000": "BTC Mainnet",
    "0110000000000000000000000000000000000000000000000000000000000000": "BTC XTN Testnet",
    "0000000000000000000000000000000000000000000000000000000000000001": "Ethereum Mainnet",
    "0000000000000000000000000000000000000000000000000000000000000038": "BNB Smart Chain",
    "0000000000000000000000000000000000000000000000000000000000aa36a7": "Ethereum Sepolia Testnet",
    "0000000000000000000000000000000000000000000000000000000000001388": "Mantle",
    "000000000000000000000000000000000000000000000000000000000000138b": "Mantle Sepolia Testnet",
}


def chain_name(chain_id):
    if type(chain_id) is int:
        name = EVM_CHAIN_ID_TO_NAME.get(chain_id, "Unknown chain")
    else:
        name = FBTC_CHAIN_ID_TO_NAME.get(chain_id, "Unknown chain")
    return f"{name} ({chain_id})"
