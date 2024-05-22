from hexbytes import HexBytes

from . import config
from .btcrpc import BitcoinRPC
from .contract import ContractFactory
from .reqdata import FBTCRequest, RequestData
from .utils import get_bridge, get_web3

REQUEST_EVENT = HexBytes("903c4021d4469fbbdf338ec3409a975e2ccbd3990776eab0750c28a16617d780")

class Verifier(object):

    def __init__(self, bridge_addr=None) -> None:
        if bridge_addr == None:
            self.bridge_addr = config.DEFAULT_BRIDGE
        else:
            self.bridge_addr = bridge_addr

        self.btcrpc = BitcoinRPC(config.DEFAULT_BTC_RPC)

    def log(self, check_item: str, result, true_msg: str = "Yes", false_msg="No"):
        self._check_index += 1
        flag = ({
            True: "[OK]",
            False: "[!!]",
            None: "[--]"
        })[result]
        msg = true_msg if result else false_msg
        print(f"({self._check_index}) {flag} {check_item}: {msg}")

    def _reset_context(self, chain_id):
        self._check_index = 0
        assert chain_id in config.FBTC_DEPLOYMENT, f"Unknown chain {chain_id}"
        rpc_url = config.FBTC_DEPLOYMENT[chain_id]["rpc"]
        self.factory = ContractFactory(rpc_url)
        self.web3 = self.factory.web3
        self.bridge = self.factory.contract(self.bridge_addr, "FireBridge")

    def _get_fbtc_request(self, chain_id, req_hash) -> FBTCRequest:
       bridge = get_bridge(chain_id, self.bridge_addr)
       return FBTCRequest(
            req_hash,
            bridge.getRequestByHash(req_hash)
        )

    def verify_request(self, data: RequestData):
        data.print()

        self._reset_context(data.chain_id)

        # Init context

        req = self._get_fbtc_request(data.chain_id, data.request_hash)
        print(req)

        if req.op_str == "Mint":
            self.verify_mint(data, req)
        elif req.op_str == "Burn":
            self.verify_burn(data, req)
        elif req.op_str == "CrosschainRequest":
            self.verify_crosschain(data, req)
        else:
            print("Unexpected request data")
            print(data)

    def _eth_tx_check(self, name, chain_id, req_hash, req_txid):
        web3 = get_web3(chain_id)
        rcpt = web3.eth.get_transaction_receipt(req_txid)
        tx_number = rcpt.blockNumber
        cur_number = web3.eth.block_number
        finalized_number = web3.eth.get_block("finalized").number
        self.log(
            f"{name} transaction confirmed",
            tx_number <= finalized_number,
            f"{cur_number - tx_number} confirmations"
        )
        event_found = False
        for log in rcpt.logs:
            if HexBytes(log.topics[0]) == REQUEST_EVENT:
                if HexBytes(log.topics[1]) == HexBytes(req_hash):
                    if log.address == self.bridge_addr:
                        event_found = True
                        break
        
        self.log(f"{name} Transaction matches the request", event_found, "Yes")

    def verify_mint(self, data: RequestData, req: FBTCRequest):

        self.log(
            "The signing tx is calling to Minter contract", 
            data.to.lower() == self.bridge.minter().lower(),
            data.to
        )
        self.log(
            "The signing tx's value is 0", 
            data.value == 0,
            data.value
        )
        self.log(
            "The signing tx's calldata is a confirmMintRequest(0x2bf90baa) call", 
            data.data[:8] == "2bf90baa",
            data.data[:8]
        )

        req_txid = data.info["add_mint_request_tx_id"]
        data_btc_txid = data.info["btc_deposit_tx_id"]

        print("AddMintRequest request hash:", req.hash)
        print("AddMintRequest txid:", req_txid)
        print("BTC Deposit txid:", data_btc_txid)

        self._eth_tx_check("AddMintRequest", data.chain_id, req.hash, req_txid)

        self.log("Request op is Mint", req.op == 1, req.op_str)
        self.log("Request status is pending", req.status == 1, req.status_str)

        btc_txid = req.extra[0:32].hex()
        vout = int.from_bytes(req.extra[32:64], "big")

        self.log(
            "BTC Deposit txid from data equals to the one from AddMintRequest", 
            data_btc_txid == btc_txid, 
            data_btc_txid,
            f"{data_btc_txid} vs {btc_txid}")
   
        btc_tx = self.btcrpc.getrawtransaction(btc_txid)

        utxo = btc_tx["vout"][vout]
        confirmations = btc_tx["confirmations"]

        self.log(
            "BTC transaction confirmations > 6",
            confirmations > 6,
            confirmations,
        )

        btc_amount = int(utxo["value"] * int(1e8))
        btc_address = utxo["scriptPubKey"]["address"]

        deposit_address = req.src_address.decode()

        self.log(
            "UTXO address equals to the deposit address",
            deposit_address == btc_address,
            f"{deposit_address} vs {btc_address}",
        )

        self.log(
            "UTXO value >= the request minting amount",
            btc_amount >= req.amount,
            f"{btc_amount} vs {req.amount}",
        )

    def verify_burn(self, data: RequestData, req: FBTCRequest):
        req_txid = data.info["add_burn_request_tx_id"]
    
        print("AddBurnRequest txid:", req_txid)
        self._eth_tx_check("AddBurnRequest", data.chain_id, req.hash, req_txid)
        self.log("Request op is Burn", req.op == 2, req.op_str)
        self.log("Request status is pending", req.status == 1, req.status_str)

        self.log(
            "Request amount equals BTC transfer amount", 
            data.value == req.amount, 
            data.value,
            f"{req.amount/1e8} vs {data.value/1e8} BTC"
        )

        req_to_addr = req.dst_address.decode('utf-8')
        self.log(
            "Request withdrawal address equals BTC transfer address", 
            data.to == req_to_addr, 
            f"{req_to_addr}",
            f"{req_to_addr} vs {data.to}"
        )

    def verify_crosschain(self, data: RequestData, req: FBTCRequest):

        req_txid = data.info["add_burn_request_tx_id"]

        print("AddCrosschainRequest txid:", req_txid)
        self._eth_tx_check("AddCrosschainRequest", req.hash, req_txid)
        self.log("Request op is CrosschainConfirm", req.op == 3, req.op_str)

        self.log(
            "All fields in ConfirmCrosschainRequest arguments, "
            "except for op, should be identical to the AddCrosschainRequest one",
            None,
            f"\n {req}"
        )
