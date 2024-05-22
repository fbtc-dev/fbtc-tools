from ..btcrpc import BitcoinRPC


def test_btc_rpc():
    rpc = BitcoinRPC()
    r = rpc.json_rpc_call("getblockcount")
    assert r > 0

    r = rpc.getblockcount()
    assert r > 0
