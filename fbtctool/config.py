BTC_RPC = {
    "btc": "https://bitcoin-mainnet.g.allthatnode.com/archive/json_rpc",
    "xtn": "https://bitcoin-testnet.g.allthatnode.com/archive/json_rpc",
}

FBTC_DEPLOYMENT = {
    11155111: {  # 0xaa36a7
        "name": "seth",
        "full": "Ethereum Sepolia Testnet",
        "rpc": "https://rpc-sepolia.rockx.com",
        "bridge": "0x0aD89E552ed249a8A60729214e8F5e483f317F47",
    },
    5003: {  # 0x138b
        "name": "smnt",
        "full": "Mantle Sepolia Testnet",
        "rpc": "https://rpc.sepolia.mantle.xyz",
        "bridge": "0x0aD89E552ed249a8A60729214e8F5e483f317F47",
    },
    5000: {  # 0x1338
        "name": "mnt",
        "full": "Mantle Mainnet",
        "rpc": "https://rpc.mantle.xyz",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
    56: {  # 0x38
        "name": "bsc",
        "full": "BNB Smart Chain Mainnet",
        "rpc": "https://rpc.ankr.com/bsc",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
    1: {  # 0x1
        "name": "eth",
        "full": "Ethereum Mainnet",
        "rpc": "https://rpc.ankr.com/eth",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
    42161: {
        "name": "arb",
        "full": "Arbitrum Mainnet",
        "rpc": "https://arb1.arbitrum.io/rpc",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
    8453: {
        "name": "base",
        "full": "Base Mainnet",
        "rpc": "https://mainnet.base.org",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
    60808: {
        "name": "bob",
        "full": "Bob Mainnet",
        "rpc": "https://rpc.gobob.xyz/",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
    146: {
        "name": "sonic",
        "full": "Sonic Mainnet",
        "rpc": "https://rpc.soniclabs.com",
        "bridge": "0xbee335BB44e75C4794a0b9B54E8027b111395943",
    },
}

DEFAULT_BTC_RPC = BTC_RPC["btc"]
DEFAULT_ETH_RPC = FBTC_DEPLOYMENT[1]["rpc"]
DEFAULT_BRIDGE = FBTC_DEPLOYMENT[1]["bridge"]
