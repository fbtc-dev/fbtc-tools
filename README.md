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
 Current Chain: Ethereum Sepolia Testnet (11155111)
 ================================================================================
 FireBridge: 0x0aD89E552ed249a8A60729214e8F5e483f317F47
     Owner: 0x1c3dA4B3B951309b618Db1C0e1745ce3C03259d2 Contract
     Pending Owner: 0x0000000000000000000000000000000000000000 EOA
     Paused: False
     FBTC: 0x037017580b1Ed99952a006b5197592B1AA08A166
     Minter: 0x50e4FC7709998E64E83BD2C1a8a37790eb90c642
     Fee Recipient: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
     Main Chain: BTC XTN Testnet (0110000000000000000000000000000000000000000000000000000000000000)
     Current Chain: Ethereum Sepolia Testnet (0000000000000000000000000000000000000000000000000000000000aa36a7)
     Cross-chain whilist:
         (1) Mantle Sepolia Testnet (000000000000000000000000000000000000000000000000000000000000138b)
     Qualified Users: 4
         (1) EVM Address: 0x0F9D6b8AFc1f64D6Eb083C1291BaD48c5785156b EOA
             Locked: False
             BTC Deposit Address: tb1qg4s0qgxv73ecq6w47arj40zxun6c98eq9u09ya
             BTC Withdrawal Address: tb1q535vz3mn0gftwcmwmaqtx9h8fdczazwrfjw3tz
         (2) EVM Address: 0x3c7eA03EcaE6AdC92Ea65c7C641590594B8571a1 EOA
             Locked: False
             BTC Deposit Address: tb1qx2flmts4mtwvf08fh8k60ts2yrueakcrkqjdyx
             BTC Withdrawal Address: tb1pvalpq2qg9qqawlcnk0pv485ccrlt9svecndfhxf4c5f77rwhyq9qfqt9yh
         (3) EVM Address: 0xF82Aff09B5e2f759989d61e9dfaebBEBD5739383 EOA
             Locked: False
             BTC Deposit Address: tb1qnaycgqr6hepatzz3j06l7pa3jd7yx85kkjveq2
             BTC Withdrawal Address: tb1pn90jxyjq60yux0wnqsjy0lfrww2e7elu3a0thy2h32u7ymqqgy6qvsz2vh
         (4) EVM Address: 0x18534DE3E074ceC40f77EAAd276fC7074f1f444a EOA
             Locked: False
             BTC Deposit Address: tb1qssjr0ky80272fcar8zytlamcdfyqh25plx0dlq
             BTC Withdrawal Address: tb1qdnx286xepp4f06gl7z4r39j2pglvcel9kun7rm
 ================================================================================
 FBTC: 0x037017580b1Ed99952a006b5197592B1AA08A166
     Bridge: 0x0aD89E552ed249a8A60729214e8F5e483f317F47
     Owner: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
     Paused: False
     Decimals: 8
     Total Supply: 0.0 FBTC
 ================================================================================
 FBTCMinter: 0x50e4FC7709998E64E83BD2C1a8a37790eb90c642
     Owner: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
     Bridge: 0x0aD89E552ed249a8A60729214e8F5e483f317F47
     Minting:
         (1) 0x5b28716dBc5294ac3dC1309B72D351AB303544Ad EOA
     Burning:
         (1) 0x4b321181A0f549D029Bf3eC0d2294BD895D6557B EOA
     Cross-chaining:
         (1) 0x848AC81BfADEcf4C5b6347fFEFB0d12C689f14aA EOA
 ================================================================================
 FeeModel: 0x99F56add13604273e91A625465ca38DBe26F22d1
     Owner: 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0
     Mint:
         Minimal: 0.0 FBTC
         Fee Rate Tiers:
             < MAX: 0.0 %
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
 ================================================================================
     Version: 1.3.0
     Threshold: 1 / 3
     Owners: 3 owners
         (1) 0x18534DE3E074ceC40f77EAAd276fC7074f1f444a EOA
         (2) 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
         (3) 0xF82Aff09B5e2f759989d61e9dfaebBEBD5739383 EOA
     Modules: 2 modules
         (1) 0xc2DEb2Fd8c647302e46AC522F8E5Cb7A93d38C25
             FBTCGovernorModule: 
             Owner: 0x1c3dA4B3B951309b618Db1C0e1745ce3C03259d2 Contract
                 Qualified User Managers:
                     (1) 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
                 FBTC Block-list Managers:
                     (1) 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
                 FBTC Pauser:
                     (1) 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
                 FireBridge Pauser:
                     (1) 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
                 Cross-chain Targets Manager:
                     (1) 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
                 Cross-chain Fee Updater:
                     (1) 0x965CebC1C9E81c951067E3905B0ce84DF34B55d0 EOA
```
