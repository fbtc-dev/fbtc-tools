from argparse import ArgumentParser

from .verifier import Verifier
from .viewer import Viewer


def main():
    parser = ArgumentParser(
        prog="fbtctool", description="A simple local FBTC relay checker"
    )

    parser.add_argument(
        "-b",
        "--btc-rpc",
        help="Bitcoin RPC endpoint.",
    )

    parser.add_argument(
        "-e",
        "--evm-rpc",
        help="EVM RPC endpoint.",
    )

    parser.add_argument(
        "-a",
        "--bridge-address",
        help="Contract address of FireBridge.",
    )

    parser.add_argument(
        "-v",
        "--view",
        action="store_true",
        help="View the contract information.",
    )
    parser.add_argument("-r", "--request-hash", help="The hash of FBTC request.")
    parser.add_argument("-t", "--txid", help="The txid of the source request.")

    args = parser.parse_args()

    
    if args.request_hash:
        assert args.txid, f"--txid not set"
        v = Verifier(args.evm_rpc, args.btc_rpc, args.bridge_address)
        v.verify_request(args.request_hash, args.txid)

    elif args.view:
        Viewer(args.evm_rpc, args.bridge_address).print()

if __name__ == "__main__":
    main()
