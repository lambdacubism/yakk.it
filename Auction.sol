// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts-upgradeable/proxy/utils/Initializable.sol";
import "@openzeppelin/contracts-upgradeable/proxy/utils/UUPSUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/access/OwnableUpgradeable.sol";
import "@openzeppelin/contracts-upgradeable/security/ReentrancyGuardUpgradeable.sol";

// Blast Network Interface
interface IBlast {
    function configureAutomaticYield() external;
    function configureClaimableYield() external;
    function claimYield(address from, address recipient, uint256 amount) external;
    function claimAllYield(address from, address recipient) external;
    function configureClaimableGas() external;
    
    // Add any other necessary functions from the Blast interface here
}
contract AuctionUpgradeable is Initializable, UUPSUpgradeable, OwnableUpgradeable, ReentrancyGuardUpgradeable {
    uint256 public auctionDuration;
    address payable public teamAddress;
    IBlast public blast; // State variable declaration for the Blast contract interface


    // Auction details struct and other state variables remain the same
    struct AuctionDetails {
        bool active;
        uint256 startingBid;
        uint256 highestBid;
        address highestBidder;
        uint256 endTime;
    }

    mapping(uint256 => AuctionDetails) public auctions;

    event AuctionStarted(uint256 indexed titleId, uint256 startingBid, uint256 endTime);
    event BidPlaced(uint256 indexed titleId, address bidder, uint256 amount);
    event BidCancelled(uint256 indexed titleId, address bidder);
    event AuctionEnded(uint256 indexed titleId, address winner, uint256 amount);

    
    // 77 hours = 77 * 60 minutes/hour * 60 seconds/minute = 277,200 seconds
    // So, when initializing the contract through the proxy, pass 277200 for _auctionDuration

    // _teamAddress is the seller of the titles, the house in another word


    function initialize(
        address payable _teamAddress,
        uint256 _auctionDuration,
        address _blastAddress // Address of the Blast contract
    ) public initializer {
        __Ownable_init(msg.sender); // msg.sender will be the initial owner !!! dikkat: Now the initialize function sets the deployer as the owner by using msg.sender, which is the address that is deploying and initializing the contract through the proxy.
        __ReentrancyGuard_init();
        teamAddress = _teamAddress;
        auctionDuration = _auctionDuration;
        blast = IBlast(_blastAddress);
        blast.configureAutomaticYield(); // Configures the contract for automatic yield with Blast Network
    }


    function _authorizeUpgrade(address newImplementation) internal override onlyOwner {}


    function startAuction(uint256 titleId, uint256 startingBid) external {
        require(!auctions[titleId].active, "Auction already active");

        AuctionDetails storage auction = auctions[titleId];
        auction.active = true;
        auction.startingBid = startingBid;
        auction.highestBid = startingBid;
        auction.highestBidder = address(0);
        auction.endTime = block.timestamp + auctionDuration;

        emit AuctionStarted(titleId, startingBid, auction.endTime);
    }

    function placeBid(uint256 titleId) external payable nonReentrant {
        AuctionDetails storage auction = auctions[titleId];
        require(auction.active, "Auction not active");
        require(block.timestamp < auction.endTime, "Auction has ended");
        require(msg.value > auction.highestBid, "Bid not high enough");

        if (auction.highestBidder != address(0)) {
            payable(auction.highestBidder).transfer(auction.highestBid);
        }

        auction.highestBid = msg.value;
        auction.highestBidder = msg.sender;

        emit BidPlaced(titleId, msg.sender, msg.value);
    }

    function cancelBid(uint256 titleId) external nonReentrant {
        AuctionDetails storage auction = auctions[titleId];
        require(auction.active, "Auction not active");
        require(auction.highestBidder == msg.sender, "Only highest bidder can cancel");

        payable(auction.highestBidder).transfer(auction.highestBid);
        
        auction.highestBid = auction.startingBid;
        auction.highestBidder = address(0);

        emit BidCancelled(titleId, msg.sender);
    }

    function finalizeAuction(uint256 titleId) external nonReentrant {
        AuctionDetails storage auction = auctions[titleId];
        require(auction.active, "Auction not active");
        require(block.timestamp >= auction.endTime, "Auction not yet ended");

        if (auction.highestBidder != address(0)) {

        // Claim all yield before transferring the highest bid
        blast.claimAllYield(address(this), teamAddress);

        // Transfer the highest bid to the team address
        teamAddress.transfer(auction.highestBid);
        
            emit AuctionEnded(titleId, auction.highestBidder, auction.highestBid);
        } else {
            emit AuctionEnded(titleId, address(0), 0);
        }

        auction.active = false;
    }

    // Update team address by the owner
    function updateTeamAddress(address payable newAddress) external onlyOwner {
        teamAddress = newAddress;
    }

    // The onlyOwner modifier comes from the OpenZeppelin OwnableUpgradeable contract, 
    // which ensures that only the current owner can execute the function it is applied to.

}

