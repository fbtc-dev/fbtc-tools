# Install

```
$ git clone https://github.com/fbtc-dev/fbtc-tools
$ cd fbtc-tools
$ pip install -r requirements.txt 
$ python -m fbtctool.main -h
```

# Usage

## Print request / user info

```sh
# Print user information
$ python -m fbtctool.main -e seth -u 0xfed1fd7e9bbe5032c872b1a162ba2d88548c0af5

# Print latest requests
$ python -m fbtctool.main -e seth -l 4
# Print latest requests related to the user
$ python -m fbtctool.main -e seth -l 4 -u 0xfed1fd7e9bbe5032c872b1a162ba2d88548c0af5

# Print request by request hash
$ python -m fbtctool.main -r 0xBA19C3EE6D5B533239F22026B652E346D9841618B55C84E32D4804F112BCC618 -e seth0xc861d9df11c38855910fdba092412e370975b98be4e06f6064fbea10fd9a3c6e

# Print requests in the transaction
$ python -m fbtctool.main -t 0xc861d9df11c38855910fdba092412e370975b98be4e06f6064fbea10fd9a3c6e -e seth
```

## View the full protocol configuration
```sh
$ python -m fbtctool.main -e seth -v
 Current Chain: Ethereum Sepolia Testnet (11155111)
 ================================================================================
 FireBridge: 0x0aD89E552ed249a8A60729214e8F5e483f317F47
     Owner: 0x1c3dA4B3B951309b618Db1C0e1745ce3C03259d2 Safe 1 / 6
     Pending Owner: 0x0000000000000000000000000000000000000000 EOA
     Paused: False
     FBTC: 0x037017580b1Ed99952a006b5197592B1AA08A166
     Minter: 0x50e4FC7709998E64E83BD2C1a8a37790eb90c642
     Fee Model: 0x99F56add13604273e91A625465ca38DBe26F22d1
     Fee Recipient: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
     Main Chain: BTC XTN Testnet (0110000000000000000000000000000000000000000000000000000000000000)
     Current Chain: Ethereum Sepolia Testnet (0000000000000000000000000000000000000000000000000000000000aa36a7)
     Cross-chain white list:
         (1) Mantle Sepolia Testnet (000000000000000000000000000000000000000000000000000000000000138b)
     Qualified Users: 14
         (1) EVM Address: 0x0F9D6b8AFc1f64D6Eb083C1291BaD48c5785156b EOA
             Locked: False
             BTC Deposit Address: tb1qg4s0qgxv73ecq6w47arj40zxun6c98eq9u09ya
             BTC Withdrawal Address: tb1q535vz3mn0gftwcmwmaqtx9h8fdczazwrfjw3tz
    ...
```

## Verify request
1. Save the request data into local file.

2. Run fbtctool
```sh
$ python -m fbtctool.main -f ./input.json
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
