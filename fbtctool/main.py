from argparse import ArgumentParser

from .verifier import RequestData, Verifier
from .viewer import Viewer


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
        help="View all the contract information of FBTC.",
    )

    parser.add_argument(
        "-l",
        "--list-requests",
        type=int,
        help="List the recent request information of the bridge.",
    )

    parser.add_argument(
        "-u",
        "--user",
        help="Get user information.",
    )

    parser.add_argument(
        "-r",
        "--req-hash",
        help="Print the request information by hash.",
    )

    parser.add_argument(
        "-t",
        "--txid",
        help="Print the FBTC request in the trasaction.",
    )

    parser.add_argument(
        "-f", "--request-file-path", help="Verify request data json file."
    )

    args = parser.parse_args()

    if args.view:
        Viewer(args.evm_rpc, args.bridge_address).print()
    elif args.req_hash:
        Viewer(args.evm_rpc, args.bridge_address).print_request(args.req_hash)
    elif args.txid:
        Viewer(args.evm_rpc, args.bridge_address).print_request_in_tx(args.txid)
    elif args.list_requests:
        Viewer(args.evm_rpc, args.bridge_address).print_requests(
            args.list_requests, args.user
        )
    elif args.user:
        Viewer(args.evm_rpc, args.bridge_address).print_user_info(args.user)
    elif args.request_file_path:
        s = open(args.request_file_path).read()
        r = RequestData(s)
        Verifier(args.btc_rpc, args.bridge_address).verify_request(r)


if __name__ == "__main__":
    main()
