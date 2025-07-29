// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "base64-sol/base64.sol";

contract LedgerSouls is ERC721, Ownable {
    using Strings for uint256;

    enum Phase {
        NewSpirit,
        Embodied,
        Reincarnated,
        Unified,
        Decohered
    }

    struct Soul {
        // Ledger State
        int256 kappa; // Recognition Debt/Surplus
        uint256 energy;
        uint256 depth; // Stored as integer, multiplied by 10 (e.g., 53.2 is stored as 532)
        uint8 rebirths;
        bool isEmbodied;
        Phase phase;

        // Virtue Technologies (Potentials)
        uint256[] virtuePotentials; // Love, Justice, Prudence, Courage, Temperance (x10)

        // Karma Metrics
        int256 recognitionFlow;
        uint256 lastUpdateTimestamp;
    }

    mapping(uint256 => Soul) private _souls;

    constructor() ERC721("Ledger Souls", "SOUL") {}

    function safeMint(address to, uint256 tokenId) public onlyOwner {
        _safeMint(to, tokenId);
        _initializeSoul(tokenId);
    }

    function _initializeSoul(uint256 tokenId) private {
        // Initial values will be set based on a deterministic seed
        // For now, we use placeholder values.
        uint256[] memory initialVirtues = new uint256[](5);
        initialVirtues[0] = 10; // Love
        initialVirtues[1] = 10; // Justice
        initialVirtues[2] = 10; // Prudence
        initialVirtues[3] = 10; // Courage
        initialVirtues[4] = 10; // Temperance

        _souls[tokenId] = Soul({
            kappa: 0,
            energy: 5000, // x10
            depth: 0,
            rebirths: 0,
            isEmbodied: false,
            phase: Phase.NewSpirit,
            virtuePotentials: initialVirtues,
            recognitionFlow: 0,
            lastUpdateTimestamp: block.timestamp
        });
    }

    // Function to evolve the soul (can be called by anyone, but changes are based on time)
    function evolve(uint256 tokenId) public {
        // Evolution logic will be implemented here.
        // It will calculate elapsed time and apply changes to the soul's state.
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
        
        Soul memory soul = _souls[tokenId];

        // This will be replaced with logic to generate the text description
        string memory description = "Soul Description Placeholder";

        string memory json = Base64.encode(
            bytes(
                string(
                    abi.encodePacked(
                        '{"name": "Ledger Soul #',
                        tokenId.toString(),
                        '", "description": "',
                        description,
                        '", "image": "data:image/svg+xml;base64,',
                        // SVG generation will be added here
                        '"}'
                    )
                )
            )
        );

        return string(abi.encodePacked("data:application/json;base64,", json));
    }
} 