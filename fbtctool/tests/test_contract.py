from ..contract import ContractFactory


def test_contract():
    bridge = ContractFactory("https://rpc-sepolia.rockx.com").contract(
        "0x7087A459925f13dd902d8FF15713142d292C776A", "FireBridge"
    )
    assert bridge.nonce() > 0
