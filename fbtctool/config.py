XTN_RPC_URL = "https://bitcoin-testnet.drpc.org"
SETH_RPC_URL = "https://rpc-sepolia.rockx.com"
SMNT_RPC_URL = "https://rpc.sepolia.mantle.xyz"

SETH_BRIDGE = "0xc11b6f1eE857E76453aa98F75f7776bb44f03265"
SMNT_BRIDGE = "0xc11b6f1eE857E76453aa98F75f7776bb44f03265"

DEFAULT_BTC_RPC = XTN_RPC_URL
DEFAULT_ETH_RPC = SETH_RPC_URL
DEFAULT_BRIDGE = SETH_BRIDGE

FBTC_DEPLOYMENT = {
    11155111: { # 0xaa36a7
        "name": "seth",
        "rpc": "https://rpc-sepolia.rockx.com",
        "bridge": "0xc11b6f1eE857E76453aa98F75f7776bb44f03265"
    },
    5003: { # 0x138b
        "name": "smnt",
        "rpc": "https://rpc.sepolia.mantle.xyz",
        "bridge": "0xc11b6f1eE857E76453aa98F75f7776bb44f03265"
    }
}