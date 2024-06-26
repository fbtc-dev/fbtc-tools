from . import config
from .contract import ContractFactory, ContractFunctionWrapper
from .reqdata import FBTCRequest
from .utils import Printer, chain_name, get_bridge

printer = Printer()
p = printer.print
indent = printer.indent


class Viewer(object):
    def __init__(self, rpc_url=None, bridge_address=None) -> None:
        if rpc_url is None:
            rpc_url = config.DEFAULT_ETH_RPC
        else:
            for cfg in config.FBTC_DEPLOYMENT.values():
                if rpc_url == cfg["name"]:
                    rpc_url = cfg["rpc"]
                    if bridge_address is None:
                        bridge_address = cfg["bridge"]
                    break

        if bridge_address is None:
            bridge_address = config.DEFAULT_BRIDGE

        self.factory = ContractFactory(rpc_url)
        self.bridge = self.factory.contract(bridge_address, "FireBridge")
        self.fbtc = self.factory.contract(self.bridge.fbtc(), "FBTC")
        self.fee_model = self.factory.contract(self.bridge.feeModel(), "FeeModel")
        self.minter = self.factory.contract(self.bridge.minter(), "FBTCMinter")

        self.dst_chains = []
        self.merchants = []
        self.FEE_RATE_BASE = 1_000_000
        self.dec = 8

    def _print_list(self, title="", items=[], is_addr=True, with_balance=False):
        if title:
            p(title)
        if items:
            with indent():
                for i, s in enumerate(items):
                    if is_addr:
                        s = self._addr_name(s, with_balance)
                    p(f"({i+1}) {s}")

    def _call_if_error(self, func):
        tmp = ContractFunctionWrapper._ignore_error
        ContractFunctionWrapper._ignore_error = False
        r = None
        e = None
        try:
            r = func()
        except Exception as _e:
            e = _e
        ContractFunctionWrapper._ignore_error = tmp
        return r, e

    def _addr_name(self, addr, with_balance=False):
        if addr is None:
            return "None"

        if len(self.factory.web3.eth.get_code(addr)) == 0:
            if with_balance:
                eth = self.factory.web3.eth.get_balance(addr)
                return f"{addr} EOA, Balance {eth/1e18} ({eth})"
            else:
                return f"{addr} EOA"
        else:
            safe = self.factory.contract(addr, "Safe")

            def _f():
                owners = safe.getOwners()
                threshold = safe.getThreshold()
                return f"{addr} Safe {threshold} / {len(owners)}"

            r, e = self._call_if_error(_f)
            if e is None:
                return r
            else:
                return f"{addr} Contract"

    def print_chain_info(self):
        chain_id = self.factory.web3.eth.chain_id
        p(f"Current Chain: {chain_name(chain_id)}")

    def print_bridge(self):
        p(f"FireBridge: {self.bridge.address}")
        with indent():
            p(f"Owner: {self._addr_name(self.bridge.owner())}")
            p(f"Pending Owner: {self._addr_name(self.bridge.pendingOwner())}")
            p(f"Paused: {self.bridge.paused()}")
            p(f"FBTC: {self.bridge.fbtc()}")
            p(f"Minter: {self.bridge.minter()}")
            p(f"Fee Model: {self.bridge.feeModel()}")
            p(f"Fee Recipient: {self._addr_name(self.bridge.feeRecipient())}")
            p(f"Main Chain: {chain_name(self.bridge.MAIN_CHAIN().hex())}")
            p(f"Current Chain: {chain_name(self.bridge.chain().hex())}")
            self.dst_chains = self.bridge.getValidDstChains()
            self._print_list(
                "Cross-chain whilist:",
                [chain_name(chain.hex()) for chain in self.dst_chains],
                False,
            )

            users = self.bridge.getQualifiedUsers()
            self.merchants = users

            p(f"Qualified Users: {len(users)}")
            for i, user in enumerate(users):
                info = self.bridge.getQualifiedUserInfo(user)
                if info:
                    with indent():
                        p(f"({i+1}) EVM Address: {self._addr_name(user)}")
                        with indent():
                            p(f"Locked: {info[0]}")
                            p(f"BTC Deposit Address: {info[1]}")
                            p(f"BTC Withdrawal Address: {info[2]}")

    def _to_btc(self, amount):
        if amount == 2**256 - 1:
            return "Uint256.MAX"

        if amount == 2**224 - 1:
            return "Uint224.MAX"

        return f"{amount / (10**self.dec)} FBTC"

    def print_fbtc(self):
        p(f"FBTC: {self.fbtc.address}")
        with indent():
            p(f"Bridge: {self.fbtc.bridge()}")
            p(f"Owner: {self._addr_name(self.fbtc.owner())}")
            p(f"Pending Owner: {self._addr_name(self.fbtc.pendingOwner())}")
            p(f"Paused: {self.fbtc.paused()}")

            self.dec = self.fbtc.decimals()

            p(f"Decimals: {self.dec}")
            p(f"Total Supply: {self._to_btc(self.fbtc.totalSupply())}")

    def print_minter(self):
        p(f"FBTCMinter: {self.minter.address}")

        with indent():
            p(f"Owner: {self._addr_name(self.minter.owner())}")
            p(f"Pending Owner: {self._addr_name(self.minter.pendingOwner())}")
            p(f"Bridge: {self.minter.bridge()}")

            BURN_ROLE = self.minter.BURN_ROLE()
            CROSSCHAIN_ROLE = self.minter.CROSSCHAIN_ROLE()
            MINT_ROLE = self.minter.MINT_ROLE()

            def pb(name, role):
                self._print_list(
                    name, self.minter.getRoleMembers(role), with_balance=True
                )

            pb("Minting:", MINT_ROLE)
            pb("Burning:", BURN_ROLE)
            pb("Cross-chaining:", CROSSCHAIN_ROLE)

    def _print_fee_cfg(self, cfg):
        if cfg is None:
            return

        with indent():
            max, min, tiers = cfg
            p(f"Maximum: {self._to_btc(max)}")
            p(f"Minimum: {self._to_btc(min)}")
            p("Fee Rate Tiers:")
            with indent():
                for tier in tiers:
                    amount = self._to_btc(tier[0])

                    p(f"< {amount}: {tier[1] * 100/ self.FEE_RATE_BASE} %")

    def print_fee(self):
        p(f"FeeModel: {self.fee_model.address}")

        with indent():
            p(f"Owner: {self._addr_name(self.fee_model.owner())}")
            p(f"Pending Owner: {self._addr_name(self.fee_model.pendingOwner())}")

            self.FEE_RATE_BASE = self.fee_model.FEE_RATE_BASE()

            MINT_OP = 1
            BURN_OP = 2
            CROSS_OP = 3

            fee = self.fee_model.getDefaultFeeConfig(MINT_OP)
            p("Mint (Default):")
            self._print_fee_cfg(fee)

            fee = self.fee_model.getDefaultFeeConfig(BURN_OP)
            p("Burn (Default):")
            self._print_fee_cfg(fee)

            fee = self.fee_model.getDefaultFeeConfig(CROSS_OP)
            p("Cross-chain (Default):")
            self._print_fee_cfg(fee)

            if self.dst_chains:
                for target in self.dst_chains:
                    fee, e = self._call_if_error(
                        lambda: self.fee_model.getCrosschainFeeConfig(target)
                    )
                    if e is None:
                        p(f"Customized cross-chaining fee for {target.hex()}:")
                        self._print_fee_cfg(fee)

            if self.merchants:
                for user in self.merchants:
                    fee, e = self._call_if_error(
                        lambda: self.fee_model.getUserBurnFeeConfig(user)
                    )
                    if e is None:
                        p(f"Customized burning fee for {user}:")
                        self._print_fee_cfg(fee)

    def print_safe(self):
        addr = self.bridge.owner()

        safe = None

        def _foo():
            nonlocal safe
            safe = self.factory.contract(addr, "Safe")
            return safe.VERSION()

        ver, e = self._call_if_error(_foo)
        if e:
            p(f"FireBridge owner is not Safe wallet {addr}")
            return

        p(f"FireBridge Owner Safe: {addr}")

        with indent():
            p(f"Version: {ver}")

            owners = safe.getOwners()
            threshold = safe.getThreshold()
            p(f"Threshold: {threshold} / {len(owners)}")
            self._print_list(f"Owners: {len(owners)} owners", owners)

            ONE = "0x0000000000000000000000000000000000000001"
            modules = safe.getModulesPaginated(ONE, 1000)
            assert modules[1] == ONE, "Too many modules"
            modules = modules[0]
            p(f"Modules: {len(modules)} modules")
            for i, module_addr in enumerate(modules):
                with indent():
                    p(f"({i+1}) {module_addr}")

                    CHAIN_MANAGER_ROLE = None
                    try:
                        module = self.factory.contract(
                            module_addr, "FBTCGovernorModule"
                        )
                        CHAIN_MANAGER_ROLE, e = self._call_if_error(
                            module.CHAIN_MANAGER_ROLE
                        )
                    except Exception:
                        pass

                    if CHAIN_MANAGER_ROLE is None:
                        p(f"[!] {module_addr} is not a FBTCGovernorModule")
                        continue

                    USER_MANAGER_ROLE = module.USER_MANAGER_ROLE()
                    LOCKER_ROLE = module.LOCKER_ROLE()
                    FBTC_PAUSER_ROLE = module.FBTC_PAUSER_ROLE()
                    BRIDGE_PAUSER_ROLE = module.BRIDGE_PAUSER_ROLE()
                    CHAIN_MANAGER_ROLE = module.CHAIN_MANAGER_ROLE()
                    FEE_UPDATER_ROLE = module.FEE_UPDATER_ROLE()
                    with indent():
                        p("FBTCGovernorModule: ")
                        p(f"Owner: {self._addr_name(module.owner())}")
                        p(f"Pending Owner: {self._addr_name(module.pendingOwner())}")
                        with indent():
                            self._print_list(
                                "Qualified User Managers:",
                                module.getRoleMembers(USER_MANAGER_ROLE),
                            )
                            self._print_list(
                                "FBTC Block-list Managers:",
                                module.getRoleMembers(LOCKER_ROLE),
                            )
                            self._print_list(
                                "FBTC Pauser:", module.getRoleMembers(FBTC_PAUSER_ROLE)
                            )
                            self._print_list(
                                "FireBridge Pauser:",
                                module.getRoleMembers(BRIDGE_PAUSER_ROLE),
                            )
                            self._print_list(
                                "Cross-chain Targets Manager:",
                                module.getRoleMembers(CHAIN_MANAGER_ROLE),
                            )
                            self._print_list(
                                "Cross-chain Fee Updater:",
                                module.getRoleMembers(FEE_UPDATER_ROLE),
                            )

    def print(self):
        ContractFunctionWrapper._ignore_error = True
        self.print_chain_info()
        printer.line()
        self.print_bridge()
        printer.line()
        self.print_fbtc()
        printer.line()
        self.print_minter()
        printer.line()
        self.print_fee()
        printer.line()
        self.print_safe()

    def print_requests(self, count=20):
        nonce = self.bridge.nonce()
        end = nonce - 1
        start = end - count + 1
        if start < 0:
            start = 0
        reqs = self.bridge.getRequestsByIdRange(start, end)
        reqs = [FBTCRequest(None, i) for i in reqs][::-1]
        for r in reqs:
            r.hash = "0x" + self.bridge.requestHashes(r.nonce).hex()
            p(f">>>> {r.nonce} {r.hash} <<<<")
            if r.status == 1:  # Pending
                p("!!! Pending !!!")

            if r.op == 3:  # CrosschainRequest
                dst_bridge = get_bridge(r.dst_chain_id, self.bridge.address)
                dst_hash = dst_bridge.crosschainRequestConfirmation(r.hash).hex()
                if dst_hash == "0" * 32:
                    p("!!! Pending !!!")
                else:
                    p(f"Confirmed: {dst_hash}")

            p("-" * 10)
            p(str(r))
            printer.line()
