import json

import requests

from . import config


class BitcoinRPC(object):
    def __init__(self, rpc_url=None) -> None:
        if rpc_url:
            self.rpc_url = rpc_url
        else:
            self.rpc_url = config.DEFAULT_BTC_RPC

    def json_rpc_call(self, method, args=[]):
        data = {"jsonrpc": "2.0", "method": method, "params": args, "id": 1}
        try:
            r = requests.post(self.rpc_url, json=data)
            content = r.content
            d = json.loads(content)
            return d["result"]
        except Exception as e:
            raise Exception(f"error in bitcoin rpc:\n{e}\nreturns {content}")

    def getblockcount(self):
        return self.json_rpc_call("getblockcount")

    def getblockchaininfo(self):
        return self.json_rpc_call("getblockchaininfo")

    def getrawtransaction(self, txid, verbose=True, blockhash=None):
        return self.json_rpc_call("getrawtransaction", [txid, verbose, blockhash])

    def decoderawtransaction(self, hexstring, iswitness=False):
        return self.json_rpc_call("decoderawtransaction", [hexstring, iswitness])
