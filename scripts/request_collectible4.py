from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account, get_breed_name, get_contract, fund_with_link, listen_for_event


breedIntValue = {
    "PUG": 0,
    "SHIBA_INU": 1,
    "ST_BERNARD": 2,
}


def request_collectible(breed="PUG"):
    dev = get_account()
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    int = breedIntValue[breed]
    fund_with_link(advanced_collectible.address)
    transaction1 = advanced_collectible.requestCollectible(int, {"from": dev})
    request_id1 = transaction1.events["RequestedCollectible"]["requestId"]
    RANDOM_NUM = 777
    vrf_contract = get_contract("vrf_coordinator")
    transaction2 = vrf_contract.callBackWithRandomness(request_id1, RANDOM_NUM, advanced_collectible.address, {"from": dev})
    print("Second coming", transaction2, "Success!")
    collectible_token_id = None
    if listen_for_event(advanced_collectible, "CollectibleMinted"):
        # minter = transaction2.events["CollectibleMinted"]["dogOwner"]
        collectible_token_id = transaction2.events["CollectibleMinted"]["randomId"]
        vrf_randomNum = transaction2.events["CollectibleMinted"]["randomNumber"]
        print(f"The VRF random number is {vrf_randomNum}")
    breedIndex = advanced_collectible.getBreed(collectible_token_id)
    breedURI = advanced_collectible.getTokenURI(collectible_token_id)
    breed_name = get_breed_name(breedIndex)
    print("Mint success!")
    print(f"You chose a {breed_name}. Your assigned tokenId is {collectible_token_id}, and tokenURI is {breedURI}. Congratulations!")

def main():
    request_collectible()