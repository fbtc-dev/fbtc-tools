# Usage

# Verify request
1. Save the request data into local file.

2. Run fbtctool
```
$ python -m fbtctool.main -r ./input.json
from: 0xde3d643b54ed4ae94ffb437e90a80d1b5254d3d5
to: 0x80b534D4bB3D809FbDA809DCB26D3f220634AED7
data: 2bf90baaaa4f000f815a82d5fc4bf9ad26b3fb180d407e541afc0208ede7b14dff27039e
value: 0
info: {'chain_id': '0x1388', 'btc_deposit_tx_id': '14d88e24f760b8f4fe898ff31d2f1bc6f9de634e99a990f8b4c569d48b63bfc6', 'bridge_request_hash': '0xaa4f000f815a82d5fc4bf9ad26b3fb180d407e541afc0208ede7b14dff27039e', 'add_mint_request_tx_id': '0x8cc19c2f709424b75093a01ecb45310093f07aa8048f8f65f91207e2eb48ef6a'}
FBTCRequest(
  hash: 0xaa4f000f815a82d5fc4bf9ad26b3fb180d407e541afc0208ede7b14dff27039e
  op: 1 (Mint)
  status: 1 (Pending)
  nonce: 0
  srcChain: 0100000000000000000000000000000000000000000000000000000000000000
  srcAddress: bc1qhj07ru9aczzn93qarqe272ref7ejuu78cz0uwj
  dstChain: 0000000000000000000000000000000000000000000000000000000000001388
  dstAddress: 0x5dda2837686f4ae7803c89e38cb5e444d28b96eb
  amount: 1100000
  fee: 0
  extra: 14d88e24f760b8f4fe898ff31d2f1bc6f9de634e99a990f8b4c569d48b63bfc60000000000000000000000000000000000000000000000000000000000000000
)
(1) [OK] The signing tx is calling to Minter contract: 0x80b534D4bB3D809FbDA809DCB26D3f220634AED7
(2) [OK] The signing tx's value is 0: 0
(3) [OK] The signing tx's selector is confirmMintRequest(0x2bf90baa): 2bf90baa
AddMintRequest request hash: 0xaa4f000f815a82d5fc4bf9ad26b3fb180d407e541afc0208ede7b14dff27039e
AddMintRequest txid: 0x8cc19c2f709424b75093a01ecb45310093f07aa8048f8f65f91207e2eb48ef6a
BTC Deposit txid: 14d88e24f760b8f4fe898ff31d2f1bc6f9de634e99a990f8b4c569d48b63bfc6
(4) [OK] AddMintRequest transaction confirmed: 2694 confirmations
(5) [OK] AddMintRequest Transaction matches the request: Yes
(6) [OK] Request op is Mint: Mint
(7) [OK] Request status is pending: Pending
(8) [OK] BTC Deposit txid from data equals to the one from AddMintRequest: 14d88e24f760b8f4fe898ff31d2f1bc6f9de634e99a990f8b4c569d48b63bfc6
(9) [OK] BTC transaction confirmations > 6: 26
(10) [OK] UTXO address equals to the deposit address: bc1qhj07ru9aczzn93qarqe272ref7ejuu78cz0uwj vs bc1qhj07ru9aczzn93qarqe272ref7ejuu78cz0uwj
(11) [OK] UTXO value >= the request minting amount: 1100000 vs 1100000
```

# View the full protocol configuration
```
$ python -m fbtctool.main -e  eth -a 0xbee335BB44e75C4794a0b9B54E8027b111395943 -v
```
