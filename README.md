# Usage

# Verify mint request
```
$ python -m fbtctool.main \
 -r 0x26FE28540FE95B8408FCC8B0D31905F553DCDDFCA9C27218E9F0D6C84B736F6A \
 -t 0x8a43eb7db5ba49c3bf1a13da14c434d5984dfa61675492f6b16b9e32aef71789 \
 -e https://rpc-sepolia.rockx.com \
 -b https://bitcoin-testnet.drpc.org \
 -a 0x9CCB09ab7812fbDd9F072E8bF76901f9025F840A
Request hash: 0x26FE28540FE95B8408FCC8B0D31905F553DCDDFCA9C27218E9F0D6C84B736F6A
AddMintRequest txid: 0x8a43eb7db5ba49c3bf1a13da14c434d5984dfa61675492f6b16b9e32aef71789
(1) [OK] AddMintRequest transaction confirmed: 512 confirmations
(2) [OK] Transaction match the request hash: Yes
(3) [OK] Request op is Mint: Mint
(4) [!!] Status is pending: Confirmed
(5) [OK] BTC transaction confirmations > 6: 70
(6) [OK] UTXO address equals to the deposit address: tb1qnaycgqr6hepatzz3j06l7pa3jd7yx85kkjveq2 vs tb1qnaycgqr6hepatzz3j06l7pa3jd7yx85kkjveq2
(7) [OK] UTXO value >= the request minting amount: 10000000 vs 10000000
```

# View the full protocol configuration
```
$ python -m fbtctool.main -v
FireBridge: 0xc11b6f1eE857E76453aa98F75f7776bb44f03265
  Owner: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0
  Pending Owner: 0x0000000000000000000000000000000000000000
  Paused: False
  FBTC: 0x3843B596d84b91f2c5366f806236C8BdD1c7A38f
  Minter: 0x7E3883048819E0A9Bc45C62CbE5cDe785A9e51fA
  Fee Recipient: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0
  Main Chain: 0110000000000000000000000000000000000000000000000000000000000000
  Current Chain: 0000000000000000000000000000000000000000000000000000000000aa36a7
  Cross-chain whilist:
    (1) 000000000000000000000000000000000000000000000000000000000000138b
  Qualified Users: 4
    (1) EVM Address: 0x0F9D6b8AFc1f64D6Eb083C1291BaD48c5785156b
        Locked: False
        BTC Deposit Address: tb1qg4s0qgxv73ecq6w47arj40zxun6c98eq9u09ya
        BTC Withdrawal Address: tb1q535vz3mn0gftwcmwmaqtx9h8fdczazwrfjw3tz
    (2) EVM Address: 0x3c7eA03EcaE6AdC92Ea65c7C641590594B8571a1
        Locked: False
        BTC Deposit Address: tb1qx2flmts4mtwvf08fh8k60ts2yrueakcrkqjdyx
        BTC Withdrawal Address: tb1pvalpq2qg9qqawlcnk0pv485ccrlt9svecndfhxf4c5f77rwhyq9qfqt9yh
    (3) EVM Address: 0xF82Aff09B5e2f759989d61e9dfaebBEBD5739383
        Locked: False
        BTC Deposit Address: tb1qnaycgqr6hepatzz3j06l7pa3jd7yx85kkjveq2
        BTC Withdrawal Address: tb1pn90jxyjq60yux0wnqsjy0lfrww2e7elu3a0thy2h32u7ymqqgy6qvsz2vh
    (4) EVM Address: 0x18534DE3E074ceC40f77EAAd276fC7074f1f444a
        Locked: False
        BTC Deposit Address: tb1qssjr0ky80272fcar8zytlamcdfyqh25plx0dlq
        BTC Withdrawal Address: tb1qdnx286xepp4f06gl7z4r39j2pglvcel9kun7rm
========================================
FBTC: 0x3843B596d84b91f2c5366f806236C8BdD1c7A38f
  Bridge: 0xc11b6f1eE857E76453aa98F75f7776bb44f03265
  Owner: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0
  Paused: False
  Decimals: 8
  Total Supply: 0.0 FBTC
========================================
Minter: 0x7E3883048819E0A9Bc45C62CbE5cDe785A9e51fA
  Owner: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0
  Bridge: 0xc11b6f1eE857E76453aa98F75f7776bb44f03265
  For Minting: 0x5b28716dBc5294ac3dC1309B72D351AB303544Ad
  For Burning: 0x4b321181A0f549D029Bf3eC0d2294BD895D6557B
  For Cross-chaining: 0x848AC81BfADEcf4C5b6347fFEFB0d12C689f14aA
========================================
FeeModel: 0x3757B1f9b4FBe18834c2f77Bb224d33dF145E6E8
  Owner: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0
  Mint:
     Minimal: 0.0 FBTC
     Fee Rate Tiers:
  Burn:
     Minimal: 0.01 FBTC
     Fee Rate Tiers:
      < 200.0 FBTC: 0.2 %
      < 500.0 FBTC: 0.16 %
      < 1000.0 FBTC: 0.12 %
      < MAX: 0.1 %
  Cross-chain (Default):
     Minimal: 0.0001 FBTC
     Fee Rate Tiers:
      < MAX: 0.01 %
========================================
```
