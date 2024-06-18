BTC_RPC = {
    "btc": "https://bitcoin-mainnet.g.allthatnode.com/archive/json_rpc",
    "xtn": "https://bitcoin-testnet.g.allthatnode.com/archive/json_rpc",
}

FBTC_DEPLOYMENT = {
    11155111: {  # 0xaa36a7
        "name": "seth",
        "rpc": "https://rpc-sepolia.rockx.com",
        "bridge": "0x0aD89E552ed249a8A60729214e8F5e483f317F47",
    },
    5003: {  # 0x138b
        "name": "smnt",
        "rpc": "https://rpc.sepolia.mantle.xyz",
        "bridge": "0x0aD89E552ed249a8A60729214e8F5e483f317F47",
    },
    5000: {  # 0x1338
        "name": "mnt",
        "rpc": "https://rpc.mantle.xyz",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
    1: {  # 0x1
        "name": "eth",
        "rpc": "https://rpc.ankr.com/eth",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
}

DEFAULT_BTC_RPC = BTC_RPC["btc"]
DEFAULT_ETH_RPC = FBTC_DEPLOYMENT[1]["rpc"]
DEFAULT_BRIDGE = FBTC_DEPLOYMENT[1]["bridge"]
