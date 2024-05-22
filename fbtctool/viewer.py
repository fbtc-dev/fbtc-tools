from . import config
from .contract import ContractFactory
from .utils import Printer, EVM_CHAIN_ID_TO_NAME, FBTC_CHAIN_ID_TO_NAME

printer = Printer()
p = printer.print
indent = printer.indent

class Viewer(object):
    def __init__(self, rpc_url=None, bridge_address=None) -> None:
        if rpc_url is None:
            rpc_url = config.DEFAULT_ETH_RPC
        if bridge_address is None:
            bridge_address = config.DEFAULT_BRIDGE

        self.factory = ContractFactory(rpc_url)
        self.bridge = self.factory.contract(bridge_address, "FireBridge")
        self.fbtc = self.factory.contract(self.bridge.fbtc(), "FBTC")
        self.fee_model = self.factory.contract(self.bridge.feeModel(), "FeeModel")
        self.minter = self.factory.contract(self.bridge.minter(), "FBTCMinter")

        self.dst_chains = []
        self.FEE_RATE_BASE = 1_000_000
        self.dec = 8

    def _print_list(self, title="", items=[]):
        if title:
            p(title)
        if items:
            with indent():
                for i, s in enumerate(items):
                    p(f"({i+1}) {s}")

    def _chain_name(self, chain_id):
        if type(chain_id) is int:
            name = EVM_CHAIN_ID_TO_NAME.get(chain_id, "Unknown chain")
        else:
            name = FBTC_CHAIN_ID_TO_NAME.get(chain_id, "Unknown chain")
        return f"{name} ({chain_id})"

    def print_chain_info(self):
        chain_id = self.factory.web3.eth.chain_id
        chain_name = self._chain_name(chain_id)
        p(f"Current Chain: {chain_name}")

    def print_bridge(self):
        p(f"FireBridge: {self.bridge.address}")
        with indent():
            p(f"Owner: {self.bridge.owner()}")
            p(f"Pending Owner: {self.bridge.pendingOwner()}")
            p(f"Paused: {self.bridge.paused()}")
            p(f"FBTC: {self.bridge.fbtc()}")
            p(f"Minter: {self.bridge.minter()}")
            p(f"Fee Recipient: {self.bridge.feeRecipient()}")
            p(f"Main Chain: {self._chain_name(self.bridge.MAIN_CHAIN().hex())}")
            p(f"Current Chain: {self._chain_name(self.bridge.chain().hex())}")
            self.dst_chains = self.bridge.getValidDstChains()
            self._print_list(f"Cross-chain whilist:", [self._chain_name(chain.hex()) for chain in self.dst_chains])

            users = self.bridge.getQualifiedUsers()

            p(f"Qualified Users: {len(users)}")
            for i, user in enumerate(users):
                info = self.bridge.getQualifiedUserInfo(user)
                if info:
                    with indent():
                        p(f"({i+1}) EVM Address: {user}")
                        with indent():
                            p(f"Locked: {info[0]}")
                            p(f"BTC Deposit Address: {info[1]}")
                            p(f"BTC Withdrawal Address: {info[2]}")

    def _to_btc(self, amount):
        return f"{amount / (10**self.dec)} FBTC"
    
    def print_fbtc(self):
        p(f"FBTC: {self.fbtc.address}")
        with indent():
            p(f"Bridge: {self.fbtc.bridge()}")
            p(f"Owner: {self.fbtc.owner()}")
            p(f"Paused: {self.fbtc.paused()}")

            self.dec = self.fbtc.decimals()

            p(f"Decimals: {self.dec}")
            p(f"Total Supply: {self._to_btc(self.fbtc.totalSupply())}")


    def print_minter(self):
        p(f"FBTCMinter: {self.minter.address}")
       
        with indent():
            p(f"Owner: {self.minter.owner()}")
            p(f"Bridge: {self.minter.bridge()}")

            BURN_ROLE = self.minter.BURN_ROLE()
            CROSSCHAIN_ROLE = self.minter.CROSSCHAIN_ROLE()
            MINT_ROLE = self.minter.MINT_ROLE()

            self._print_list("Minting:", self.minter.getRoleMembers(MINT_ROLE))
            self._print_list("Burning:", self.minter.getRoleMembers(BURN_ROLE))
            self._print_list("Cross-chaining:",self.minter.getRoleMembers(CROSSCHAIN_ROLE))

    def _print_fee_cfg(self, cfg):
        with indent():
            p(f"Minimal: {self._to_btc(cfg[0])}")
            p(f"Fee Rate Tiers:")
            with indent():
                for tier in cfg[1]:
                    amount = tier[0]
                    if amount == 2**224-1:
                        amount = "MAX"
                    else:
                        amount = self._to_btc(tier[0])
                    
                    p(f"< {amount}: {tier[1] * 100/ self.FEE_RATE_BASE} %")

    def print_fee(self):
        p(f"FeeModel: {self.fee_model.address}")

        with indent():
            p(f"Owner: {self.fee_model.owner()}")

            self.FEE_RATE_BASE = self.fee_model.FEE_RATE_BASE()

            MINT_OP = 1
            BURN_OP = 2
            CROSS_OP = 3

            fee = self.fee_model.getDefaultFeeConfig(MINT_OP)
            p("Mint:")
            self._print_fee_cfg(fee)

            fee = self.fee_model.getDefaultFeeConfig(BURN_OP)
            p("Burn:")
            self._print_fee_cfg(fee)


            fee = self.fee_model.getDefaultFeeConfig(CROSS_OP)
            p("Cross-chain (Default):")
            self._print_fee_cfg(fee)

            if self.dst_chains:
                for target in self.dst_chains:
                    fee = self.fee_model.getChainFeeConfig(CROSS_OP, target)
                    if fee[1]:
                        p(f"Cross-chain to {target.hex()}:")
                        self._print_fee_cfg(fee)

    def print_safe(self):
        try:
            addr = self.bridge.owner()
            safe = self.factory.contract(addr, "Safe")
            ver = safe.VERSION()
        except Exception as e:
            print(f"[!] FireBridge owner {addr} may be not a Safe wallet")
            return
        
        p(f"FireBridge Owner Safe: {addr}")

        with indent():
            owners = safe.getOwners()
            threshold = safe.getThreshold()
            p(f"Version: {ver}")
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

                    try:
                        module = self.factory.contract(module_addr, "FBTCGovernorModule")
                        USER_MANAGER_ROLE = module.USER_MANAGER_ROLE()
                    except Exception as e:
                        p(f"[!] {module_addr} is not a FBTCGovernorModule")
                        return
                    
                    LOCKER_ROLE = module.LOCKER_ROLE()
                    FBTC_PAUSER_ROLE = module.FBTC_PAUSER_ROLE()
                    BRIDGE_PAUSER_ROLE = module.BRIDGE_PAUSER_ROLE()
                    CHAIN_MANAGER_ROLE = module.CHAIN_MANAGER_ROLE()
                    FEE_UPDATER_ROLE =  module.FEE_UPDATER_ROLE()
                    with indent():
                        p("FBTCGovernorModule: ")
                        p(f"Owner: {module.owner()}")
                        with indent():
                            self._print_list("Qualified User Managers:", module.getRoleMembers(USER_MANAGER_ROLE))
                            self._print_list("FBTC Block-list Managers:", module.getRoleMembers(LOCKER_ROLE))
                            self._print_list("FBTC Pauser:", module.getRoleMembers(FBTC_PAUSER_ROLE))
                            self._print_list("FireBridge Pauser:", module.getRoleMembers(BRIDGE_PAUSER_ROLE))
                            self._print_list("Cross-chain Targets Manager:", module.getRoleMembers(CHAIN_MANAGER_ROLE))
                            self._print_list("Cross-chain Fee Updater:", module.getRoleMembers(FEE_UPDATER_ROLE))

    def print(self):
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



