// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <=0.8.13;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

//Note: ERC721URIStorage also extends all the functions of ERC721 contract
contract AdvancedCollectible is ERC721URIStorage, VRFConsumerBase {
    uint256 public tokenCounter;
    uint256 public collectibleId;

    struct CollectibleInfo {
        string URI;
        Breed breed;
    }

    enum Breed{PUG, SHIBA_INU, ST_BERNARD}
    // add other things
    mapping(bytes32 => address) public requestIdToSender;
    mapping(address => Breed) public collectorToBreed;
    mapping(uint256 => CollectibleInfo) public IdToCollectibleInfo;
    mapping(Breed => uint[]) public breedToTokenIds;
    uint[] private unMinedIds;
    event RequestedCollectible(bytes32 indexed requestId, address indexed owner); 
    event CollectibleCreated(uint indexed Id, address indexed creator); 
    // New event from the video!
    event CollectibleMinted(address indexed minter, uint indexed randomId, uint256 indexed randomNumber);


    bytes32 internal keyHash;
    uint256 internal fee;
    address private admin;
    
    constructor(address _VRFCoordinator, address _LinkToken, bytes32 _keyhash)
    VRFConsumerBase(_VRFCoordinator, _LinkToken)
    ERC721("Dogie", "DOG")
    {
        // tokenCounter = 0;
        keyHash = _keyhash;
        fee = 0.1 * 10 ** 18;
        admin = msg.sender;
    }

    modifier onlyAdmin{
        require(msg.sender == admin);
        _;
    }

    function createCollectible(string memory tokenURI, Breed _breed) onlyAdmin public {
        IdToCollectibleInfo[collectibleId] = CollectibleInfo(tokenURI, _breed);
        breedToTokenIds[_breed].push(collectibleId);
        emit CollectibleCreated(collectibleId, msg.sender);
        collectibleId += 1;
    }

    function requestCollectible(uint _breed) public returns(bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        collectorToBreed[msg.sender] = Breed(_breed);
        emit RequestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber) internal override {
        address dogOwner = requestIdToSender[requestId];
        Breed breed = collectorToBreed[dogOwner];

        uint[] memory IdsArray = breedToTokenIds[breed]; //get all the ids for this particular breed

        for(uint index = 0; index < IdsArray.length; index++){
            uint newItemId = IdsArray[index];
            if(!_exists(newItemId)){
                unMinedIds.push(newItemId);
            }
        }

        uint num = (randomNumber % unMinedIds.length);
        uint randomId = unMinedIds[num];
        CollectibleInfo memory ItemInfo = IdToCollectibleInfo[randomId];
        _safeMint(dogOwner, randomId);
        setTokenURI(randomId, ItemInfo.URI);  
        emit CollectibleMinted(dogOwner, randomId, randomNumber);
        unMinedIds = new uint[](0);
        tokenCounter = tokenCounter + 1;
        return;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) internal {
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: transfer caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    function getTokenURI(uint _tokenId) public view returns (string memory) {
        CollectibleInfo memory info = IdToCollectibleInfo[_tokenId];
        return info.URI;
    }

    function getBreed(uint _tokenId) public view returns (Breed) {
        CollectibleInfo memory info = IdToCollectibleInfo[_tokenId];
        return info.breed;
    }
}
