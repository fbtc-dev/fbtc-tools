XTN_RPC_URL = "https://bitcoin-testnet.drpc.org"

FBTC_DEPLOYMENT = {
    11155111: { # 0xaa36a7
        "name": "seth",
        "rpc": "https://rpc-sepolia.rockx.com",
        "bridge": "0x0aD89E552ed249a8A60729214e8F5e483f317F47"
    },
    5003: { # 0x138b
        "name": "smnt",
        "rpc": "https://rpc.sepolia.mantle.xyz",
        "bridge": "0x0aD89E552ed249a8A60729214e8F5e483f317F47"
    }
}

DEFAULT_BTC_RPC = XTN_RPC_URL
DEFAULT_ETH_RPC = FBTC_DEPLOYMENT[11155111]["rpc"]
DEFAULT_BRIDGE = FBTC_DEPLOYMENT[11155111]["bridge"]