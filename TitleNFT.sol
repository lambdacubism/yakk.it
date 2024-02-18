// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";

contract ForumTitleNFT is ERC721URIStorage, Ownable {
    using Counters for Counters.Counter;
    Counters.Counter private _tokenIds;

    // Mapping from token ID to metadata content
    mapping(uint256 => string) private _metadataContent;

    event TitleCreated(uint256 indexed tokenId, address creator);
    event EntryAdded(uint256 indexed tokenId, string entry);

    constructor() ERC721("ForumTitleNFT", "FTN") {}

    // Function to create a new title NFT
    function createTitle(string memory initialEntry) public returns (uint256) {
        _tokenIds.increment();

        uint256 newTitleId = _tokenIds.current();
        _mint(msg.sender, newTitleId);
        _setTokenURI(newTitleId, formatMetadata(initialEntry));

        emit TitleCreated(newTitleId, msg.sender);
        return newTitleId;
    }

    // Function to add an entry to a title NFT
    function addEntry(uint256 tokenId, string memory newEntry) public {
        require(_exists(tokenId), "ForumTitleNFT: Title does not exist.");
        require(ownerOf(tokenId) == msg.sender, "ForumTitleNFT: Only the owner can add entries.");

        string memory currentMetadata = _metadataContent[tokenId];
        _metadataContent[tokenId] = string(abi.encodePacked(currentMetadata, "\n", newEntry));
        _setTokenURI(tokenId, formatMetadata(_metadataContent[tokenId]));

        emit EntryAdded(tokenId, newEntry);
    }

    // Helper function to format metadata
    // In a production scenario, this would likely involve IPFS or similar
    function formatMetadata(string memory metadataContent) private pure returns (string memory) {
        // Format or update the metadata content. This is a simplified example.
        // You would actually want to update an off-chain metadata file or use a service like IPFS.
        return string(abi.encodePacked("data:application/json;base64,", base64(bytes(metadataContent))));
    }

    // Helper function to encode in Base64
    function base64(bytes memory data) private pure returns (string memory) {
        // Encoding data in Base64. Implementation details omitted for brevity.
        // You would use a library or implement this according to the Base64 standard.
    }
}
