from . import config
from .contract import ContractFactory

p = print

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

    def print_bridge(self):
        p(f"FireBridge: {self.bridge.address}")
        p(f"  Owner: {self.bridge.owner()}")
        p(f"  Pending Owner: {self.bridge.pendingOwner()}")
        p(f"  Paused: {self.bridge.paused()}")
        p(f"  FBTC: {self.bridge.fbtc()}")
        p(f"  Minter: {self.bridge.minter()}")
        p(f"  Fee Recipient: {self.bridge.feeRecipient()}")
        p(f"  Main Chain: {self.bridge.MAIN_CHAIN().hex()}")
        p(f"  Current Chain: {self.bridge.chain().hex()}")
        self.dst_chains = self.bridge.getValidDstChains()
        p(f"  Cross-chain whilist:")
        for i, chain in enumerate(self.dst_chains):
            p(f"    ({i+1}) {chain.hex()}")
        users = self.bridge.getQualifiedUsers()

        p(f"  Qualified Users: {len(users)}")
        for i, user in enumerate(users):
            info = self.bridge.getQualifiedUserInfo(user)
            p(f"    ({i+1}) EVM Address: {user}")
            p(f"        Locked: {info[0]}")
            p(f"        BTC Deposit Address: {info[1]}")
            p(f"        BTC Withdrawal Address: {info[2]}")

    def _to_btc(self, amount):
        return f"{amount / (10**self.dec)} FBTC"
    
    def print_fbtc(self):
        p(f"FBTC: {self.fbtc.address}")
        p(f"  Bridge: {self.fbtc.bridge()}")
        p(f"  Owner: {self.fbtc.owner()}")
        p(f"  Paused: {self.fbtc.paused()}")

        self.dec = self.fbtc.decimals()

        p(f"  Decimals: {self.dec}")
        p(f"  Total Supply: {self._to_btc(self.fbtc.totalSupply())}")


    def print_minter(self):
        p(f"Minter: {self.minter.address}")
        p(f"  Owner: {self.minter.owner()}")
        p(f"  Bridge: {self.minter.bridge()}")

        BURN_ROLE = self.minter.BURN_ROLE()
        CROSSCHAIN_ROLE = self.minter.CROSSCHAIN_ROLE()
        MINT_ROLE = self.minter.MINT_ROLE()

        p(f"  For Minting: {' '.join(self.minter.getRoleMembers(MINT_ROLE))}")
        p(f"  For Burning: {' '.join(self.minter.getRoleMembers(BURN_ROLE))}")
        p(f"  For Cross-chaining: {' '.join(self.minter.getRoleMembers(CROSSCHAIN_ROLE))}")


    def _print_fee_cfg(self, cfg):
        p(f"     Minimal: {self._to_btc(cfg[0])}")
        p(f"     Fee Rate Tiers:")
        for tier in cfg[1]:
            amount = tier[0]
            if amount == 2**224-1:
                amount = "MAX"
            else:
                amount = self._to_btc(tier[0])
            p(f"      < {amount}: {tier[1] * 100/ self.FEE_RATE_BASE} %")

    def print_fee(self):
        p = print
        p(f"FeeModel: {self.fee_model.address}")
        p(f"  Owner: {self.fee_model.owner()}")

        self.FEE_RATE_BASE = self.fee_model.FEE_RATE_BASE()

        MINT_OP = 1
        BURN_OP = 2
        CROSS_OP = 3

        fee = self.fee_model.getDefaultFeeConfig(MINT_OP)
        p("  Mint:")
        self._print_fee_cfg(fee)

        fee = self.fee_model.getDefaultFeeConfig(BURN_OP)
        p("  Burn:")
        self._print_fee_cfg(fee)


        fee = self.fee_model.getDefaultFeeConfig(CROSS_OP)
        p("  Cross-chain (Default):")
        self._print_fee_cfg(fee)

        if self.dst_chains:
            for target in self.dst_chains:
                fee = self.fee_model.getChainFeeConfig(CROSS_OP, target)
                if fee[1]:
                    p(f"  Cross-chain to {target.hex()}:")
                    self._print_fee_cfg(fee)

    def print_safe(self):
        try:
            addr = self.bridge.owner()
            safe = self.factory.contract(addr, "Safe")
            ver = safe.VERSION()
        except Exception as e:
            print(f"[!] FireBridge owner {addr} may be not a Safe wallet")
            return
    
        p = print
        p(f"Safe: {addr}")

        owners = safe.getOwners()
        threshold = safe.getThreshold()
        p(f"  Version: {ver}")
        p(f"  Threshold: {threshold} / {len(owners)}")
        p(f"  Owners: {len(owners)} owners")
        for i, owner in enumerate(owners):
            p(f"  ({i+1}) {owner}")
        
        ONE = "0x0000000000000000000000000000000000000001"
        modules = safe.getModulesPaginated(ONE, 1000)
        assert modules[1] == ONE, "Too many modules"
        modules = modules[0]
        p(f"  Modules: {len(modules)} modules")
        for i, module_addr in enumerate(modules):
            p(f"  ({i+1}) {module_addr}")

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
            p("      FBTCGovernorModule: ")
            p(f"        Owner: {module.owner()}")
            p(f"        Qualified User Managers: {' '.join(module.getRoleMembers(USER_MANAGER_ROLE))}")
            p(f"        FBTC Block-list Managers: {' '.join(module.getRoleMembers(LOCKER_ROLE))}")
            p(f"        FBTC Pauser: {' '.join(module.getRoleMembers(FBTC_PAUSER_ROLE))}")
            p(f"        FireBridge Pauser: {' '.join(module.getRoleMembers(BRIDGE_PAUSER_ROLE))}")
            p(f"        Cross-chain Targets Manager: {' '.join(module.getRoleMembers(CHAIN_MANAGER_ROLE))}")
            p(f"        Cross-chain Fee Updater: {' '.join(module.getRoleMembers(FEE_UPDATER_ROLE))}")


    def print(self):
        self.print_bridge()
        print('='* 40)
        self.print_fbtc()
        print('='* 40)
        self.print_minter()
        print('='* 40)
        self.print_fee()
        print('='* 40)
        self.print_safe()



