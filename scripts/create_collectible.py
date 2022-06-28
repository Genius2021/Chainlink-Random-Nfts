#!/usr/bin/python3
from brownie import AdvancedCollectible
from scripts.helpful_scripts import get_account, get_breed_name, fund_with_link, listen_for_event
from scripts.dog_tokenURI_dict import tokenURI_mappings
from scripts.create_metadata import write_metadata
import time

breedIntValue = {
    "PUG": 0,
    "SHIBA_INU": 1,
    "ST_BERNARD": 2,
}

def main():
    dev = get_account()
    print("akant is",dev)
    advanced_collectible = AdvancedCollectible[len(AdvancedCollectible) - 1]

    for name in tokenURI_mappings: #Object mapping
        uriArray = tokenURI_mappings[name] #Array looping
        for uri in uriArray:
            # write_metadata(number_of_collectibles)
            int = breedIntValue[name]
            transaction = advanced_collectible.createCollectible(uri, int , {"from": dev})
            print("The transaction info is", transaction)
            print("Waiting for block confirmation...")
            # wait for the 2nd transaction
            transaction.wait(1)
            # time.sleep(35)
            # listen_for_event(
            #     advanced_collectible, "ReturnedCollectible", timeout=200, poll_interval=10
            # )
            token_id = transaction.events["CollectibleCreated"]["Id"]
            breedIndex = advanced_collectible.getBreed(token_id)
            breed_name = get_breed_name(breedIndex) #This line basically maps the id to breed name. Because the Breed type returns an integer to the frontend. 
            print(breed_name, token_id)
            print(f"Dog breed of tokenId {token_id} is {breed_name}")
            print(f"Collectible with id {token_id} created!")
