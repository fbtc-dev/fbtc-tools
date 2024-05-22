import json

from .utils import get_bridge

class FBTCRequest(object):
    OP = {
        0: "Nop",
        1: "Mint",
        2: "Burn",
        3: "CrosschainRequest",
        4: "CrosschainConfirm",
    }

    STATUS = {0: "Unused", 1: "Pending", 2: "Confirmed", 3: "Rejected"}

    def __init__(self, hash, raw_tuple) -> None:
        self.hash = hash
        (
            self.op,
            self.status,
            self.nonce,
            self.src_chain,
            self.src_address,
            self.dst_chain,
            self.dst_address,
            self.amount,
            self.fee,
            self.extra,
        ) = raw_tuple

    def __repr__(self) -> str:
        op_str = self.OP[self.op]
        status_str = self.STATUS[self.status]
        return f"FBTCRequest({op_str}, {status_str}, {self.nonce})"

    def _norm_addr(self, b: bytes) -> str:
        if len(b) == 32 and b.startswith(b"\x00" * 12):
            return "0x" + b[12:].hex()
        s = b.decode("unicode-escape")
        if s.isprintable():
            return s
        else:
            return b.hex()

    def __str__(self) -> str:
        s = "FBTCRequest(\n"
        s += f"  hash: {self.hash}\n"
        s += f"  op: {self.op} ({self.op_str})\n"
        s += f"  status: {self.status} ({self.status_str})\n"
        s += f"  nonce: {self.nonce}\n"
        s += f"  srcChain: {self.src_chain.hex()}\n"
        s += f"  srcAddress: {self._norm_addr(self.src_address)}\n"
        s += f"  dstChain: {self.dst_chain.hex()}\n"
        s += f"  dstAddress: {self._norm_addr(self.dst_address)}\n"
        s += f"  amount: {self.amount}\n"
        s += f"  fee: {self.fee}\n"
        s += f"  extra: {self.extra.hex()}\n"
        s += ")"
        return s

    @property
    def op_str(self):
        return self.OP[self.op]

    @property
    def status_str(self):
        return self.STATUS[self.status]
    

class RequestData(object):

    def __init__(self, raw_str: str) -> None:
        self.raw = json.loads(raw_str)["raw_data"]

        self.sender = self.raw["from_address"]
        self.to = self.raw["to_address"]
        self.value = int(self.raw["amount"])

        extra = self.raw["extra_parameters"]
        if extra:
            self.data = json.loads(extra).get("calldata")
        else:
            self.data = None

        note = self.raw["note"]
        assert note

        self.info = json.loads(note)["bridge_tx_info"]
        self.chain_id = int(self.info["chain_id"], 16)
        self.request_hash = self.info["bridge_request_hash"]

    def print(self):
        print("from:", self.sender)
        print("to:", self.to)
        print("data:", self.data)
        print("value:", self.value)
        print("info:", self.info)