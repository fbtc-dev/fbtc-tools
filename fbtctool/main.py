from argparse import ArgumentParser

from .verifier import Verifier, RequestData
from .viewer import Viewer
from .utils import read_json


def main():
    parser = ArgumentParser(
        prog="fbtctool", description="A simple local FBTC relay checker"
    )

    parser.add_argument(
        "-b",
        "--btc-rpc",
        help="Bitcoin RPC endpoint. URL or alias: btc, xtn",
    )

    parser.add_argument(
        "-e",
        "--evm-rpc",
        help="EVM RPC endpoint. URL or alias: eth, seth, mnt, smnt.",
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
    parser.add_argument(
        "-r", 
        "--request-file-path", 
        help="Verify request data json file."
    )

    args = parser.parse_args()
    
    if args.view:
        Viewer(args.evm_rpc, args.bridge_address).print()
    elif args.request_file_path:
        s = open(args.request_file_path).read()
        r = RequestData(s)
        Verifier(args.btc_rpc, args.bridge_address).verify_request(r)

if __name__ == "__main__":
    main()
