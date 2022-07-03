#!/usr/bin/python3
from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account, get_breed_name, listen_for_event
from scripts.create_metadata2 import write_metadata
import time
import json

breedIntValue = {
    "PUG": 0,
    "SHIBA_INU": 1,
    "ST_BERNARD": 2,
}

def main():
    dev = get_account()
    print("Boss! The active account is",dev)
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]
    with open("scripts/tokenURI_dict.json", "r") as file:
        tokenURI_dict = json.load(file)

        for name in tokenURI_dict: #Object mapping
            uriArray = tokenURI_dict[name] #Array looping
            for uri in uriArray:
                int = breedIntValue[name]
                transaction = advanced_collectible.createCollectible(uri, int , {"from": dev})
                print("The transaction info is", transaction)
                print("Waiting for block confirmation...")
                transaction.wait(1)
                # time.sleep(35)
                # listen_for_event(
                #     advanced_collectible, "ReturnedCollectible", timeout=200, poll_interval=10
                # )
                token_id = transaction.events["CollectibleCreated"]["Id"]
                breedIndex = advanced_collectible.getBreed(token_id)
                breed_name = get_breed_name(breedIndex) #This line basically maps the id to breed name. Because the Breed type returns an integer to the frontend. 
                print(breed_name, token_id)
                print(f"Dog breed of tokenId {token_id} and breedName {breed_name} has been created!")
                count = advanced_collectible.collectibleId()
                print(f"Created a total of {count} collectibles!")
