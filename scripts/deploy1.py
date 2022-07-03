#!/usr/bin/python3
from brownie import AdvancedCollectible, network, config
from scripts.helpful_scripts import fund_with_link, get_account, get_publish_source, get_contract

def main():
    dev = get_account()
    print(network.show_active())
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        {"from": dev},
        publish_source=get_publish_source(),
    )
    print("Advanced collectible deployed at: ", advanced_collectible.address)
    fund_with_link(advanced_collectible.address)
    return advanced_collectible
