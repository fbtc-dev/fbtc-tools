import json

from .utils import chain_name


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
        s += f"  srcChain: {self.src_chain_name}\n"
        s += f"  srcAddress: {self.normalized_src_addr}\n"
        s += f"  dstChain: {self.dst_chain_name}\n"
        s += f"  dstAddress: {self.normalized_dst_addr}\n"
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

    @property
    def src_chain_id(self):
        return int(self.src_chain.hex(), 16)

    @property
    def dst_chain_id(self):
        return int(self.dst_chain.hex(), 16)

    @property
    def src_chain_name(self):
        return chain_name(self.src_chain.hex())

    @property
    def dst_chain_name(self):
        return chain_name(self.dst_chain.hex())

    @property
    def normalized_src_addr(self):
        return self._norm_addr(self.src_address)

    @property
    def normalized_dst_addr(self):
        return self._norm_addr(self.dst_address)


class RequestData(object):
    def __init__(self, raw_str: str) -> None:
        self.raw = json.loads(raw_str.strip())
        self.raw_data = self.raw["raw_data"]

        self.sender = self.raw_data["from_address"]
        self.to = self.raw_data["to_address"]
        self.value = int(self.raw_data["amount"])

        extra = self.raw_data["extra_parameters"]
        if extra:
            self.data = json.loads(extra).get("calldata")
        else:
            self.data = None

        note = self.raw_data["note"]
        assert note

        self.info = json.loads(note)["bridge_tx_info"]
        self.chain_id = int(self.info["chain_id"], 16)
        self.request_hash = self.info.get("bridge_request_hash")

    def __str__(self) -> str:
        s = "RequestData(\n"
        s += f"  from: {self.sender}\n"
        s += f"  to: {self.to}\n"
        s += f"  data: {self.data}\n"
        s += f"  value: {self.value}\n"
        s += f"  info: {self.info}\n"
        s += ")"
        return s
