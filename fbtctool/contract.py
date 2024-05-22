import json
import os
from typing import Any

from web3 import Web3

from . import config


class ContractFunctionWrapper(object):
    def __init__(self, web3, func, sender) -> None:
        self.web3 = web3
        self.func = func
        self.abi = func.abi
        self.is_view = func.abi.get("stateMutability") in ["view", "pure"]
        self.sender = sender

    def __repr__(self) -> str:
        return repr(self.func)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        if self.is_view:
            return self.call(*args, **kwds)
        else:
            return self.transact(*args, **kwds)

    def _split_args(self, args):
        """
        The last arg is TxParam
        """
        if self.sender:
            tx_args = {"from": self.sender}
        else:
            tx_args = {}

        if len(args) == 0:
            return args, tx_args

        last_arg = args[-1]
        if isinstance(last_arg, dict):  # dict-like
            tx_args.update(last_arg)
            args = args[:-1]
        return args, tx_args

    def call(self, *args: Any, **kwds: Any) -> Any:
        args, tx_args = self._split_args(args)
        return self.func(*args, **kwds).call(tx_args)

    def transact(self, *args: Any, **kwds: Any) -> Any:
        args, tx_args = self._split_args(args)

        sender = tx_args.get("from", None)

        if sender is None:
            tx_args["from"] = self.sender

        tx_hash = self.func(*args, **kwds).transact(tx_args)
        receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        assert receipt["status"] == 1, f"{tx_hash} reverted"
        return receipt

    def build(self, *args: Any, **kwds: Any) -> Any:
        args, tx_args = self._split_args(args)
        return self.func(*args, **kwds).build_transaction(tx_args)


class ContractWrapper(object):
    _CONTRACT_CHECK_CACHE = set()

    def __init__(self, web3, address, abi=None, sender=None) -> None:
        self.web3 = web3
        self.address = self.web3.toChecksumAddress(address)

        if self.address not in ContractWrapper._CONTRACT_CHECK_CACHE:
            assert (
                len(self.web3.eth.get_code(self.address)) > 0
            ), f"Not contract deployed at {self.address}"
            ContractWrapper._CONTRACT_CHECK_CACHE.add(self.address)

        self.sender = sender
        self.abi = abi

        self.contract = self.web3.eth.contract(address=self.address, abi=self.abi)

        self._bind_methods()

    def _bind_methods(self):
        for fn in self.contract.all_functions():
            if getattr(self, fn.fn_name, None):
                # print(f"[!] {fn.fn_name} name collision bound.")
                continue
            setattr(
                self, fn.fn_name, ContractFunctionWrapper(self.web3, fn, self.sender)
            )

    def get_by_sig(self, sig):
        fn = self.contract.get_function_by_signature(sig)
        return ContractFunctionWrapper(fn, self.sender)


class ContractFactory(object):
    def __init__(self, rpc_url=None) -> None:
        if rpc_url:
            self.rpc_url = rpc_url
        else:
            self.rpc_url = config.DEFAULT_ETH_RPC

        self.web3 = Web3(Web3.HTTPProvider(rpc_url))

    def load_abi(self, abi) -> list:
        if type(abi) is str:
            if abi.strip().startswith("["):
                abi = json.loads(abi)
            else:
                path = os.path.dirname(__file__)
                path = os.path.join(path, "abi", f"{abi}.json")
                data = open(path).read()
                abi = json.loads(data)

        assert type(abi) is list, "Invalid abi"
        return abi

    def contract(self, address, abi) -> ContractWrapper:
        abi = self.load_abi(abi)
        return ContractWrapper(self.web3, address, abi)
