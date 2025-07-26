// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "@openzeppelin/contracts/utils/Base64.sol";

contract LedgerSouls is ERC721, ERC721Enumerable, Ownable {
    using Strings for uint256;
    using Strings for int256;

    uint256 public constant TOTAL_SUPPLY = 10000;
    uint256 public constant PHI = 1618; // φ * 1000

    struct SoulState {
        int256 kappa;
        uint256[5] virtues;
        uint256 depth;
        uint256 rebirths;
        uint256 cri;
        string qualia;
        string phase;
    }

    constructor() ERC721("Ledger Souls", "SOUL") {}

    function _baseURI() internal pure override returns (string memory) {
        return "https://api.recognitionsceince.com/souls/";
    }

    function mint(address to, uint256 quantity) public payable {
        uint256 currentSupply = totalSupply();
        require(currentSupply + quantity <= TOTAL_SUPPLY, "Max supply exceeded");
        for (uint256 i = 0; i < quantity; i++) {
            _safeMint(to, currentSupply + i);
        }
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        require(_exists(tokenId), "URI query for nonexistent token");

        SoulState memory state = getCurrentState(tokenId);

        string memory textContent = generateTextDescription(tokenId, state);
        string memory svg = generateSVG(textContent);
        
        string memory json = Base64.encode(
            bytes(
                string.concat(
                    '{"name": "Ledger Soul #',
                    tokenId.toString(),
                    '", "description": "An on-chain soul evolving according to the principles of Recognition Science. Its state is dynamically generated and changes over time.", "image": "data:image/svg+xml;base64,',
                    Base64.encode(bytes(svg)),
                    '"}'
                )
            )
        );

        return string.concat("data:application/json;base64,", json);
    }
    
    function generateSVG(string memory textContent) internal pure returns (string memory) {
        string memory svg = string.concat(
            '<svg width="500" height="500" xmlns="http://www.w3.org/2000/svg">',
            '<rect width="100%" height="100%" fill="black" />',
            '<text y="50" font-family="monospace" font-size="14" fill="white">',
            '<tspan x="50">', textContent, '</tspan>',
            '</text>',
            '</svg>'
        );
        return svg;
    }

    function generateTextDescription(uint256 tokenId, SoulState memory state) internal pure returns (string memory) {
        return string.concat(
            "SOUL #", tokenId.toString(), "\\n\\n",
            "STATE: ", state.phase, "\\n",
            "QUALIA: ", state.qualia, "\\n\\n",
            "--- METRICS ---\\n",
            "Curvature (Kappa): ", state.kappa.toString(), "\\n",
            "Depth: ", state.depth.toString(), "\\n",
            "Rebirths: ", state.rebirths.toString(), "\\n",
            "CRI: ", state.cri.toString(), "\\n\\n",
            "--- VIRTUES ---\\n",
            "Love:       ", state.virtues[0].toString(), "\\n",
            "Justice:    ", state.virtues[1].toString(), "\\n",
            "Wisdom:     ", state.virtues[2].toString(), "\\n",
            "Courage:    ", state.virtues[3].toString(), "\\n",
            "Temperance: ", state.virtues[4].toString()
        );
    }

    function getCurrentState(uint256 tokenId) public view returns (SoulState memory) {
        uint256 seed = uint256(keccak256(abi.encodePacked(tokenId, block.chainid)));
        uint256 months = (block.timestamp / 30 days); // Simplified for on-chain
        if (months > 96) {
            months = 96;
        }

        // --- All the evolution logic from JS translated to Solidity ---
        // (This is a simplified version for demonstration)

        int256 chaos = int256((uint256(blockhash(block.number - 1)) % 41)) - 20;
        int256 initialKappa = int256((seed % 200)) - 100;
        int256 kappa = initialKappa + (chaos * 10) - int256(months * 10);
        
        uint256[5] memory virtues;
        for(uint i=0; i<5; i++){
            virtues[i] = (seed >> (i*8)) % 5 + months;
            if (virtues[i] > 10) virtues[i] = 10;
        }

        uint256 rebirths = months / 8;
        uint256 depth = months + (rebirths * PHI / 100);

        string memory qualia = "Observing the cosmic ledger.";
        if (kappa > 500) {
            qualia = "Experiencing imbalance and suffering.";
        } else if (kappa < -500) {
            qualia = "Flowing in a state of surplus and harmony.";
        }
        
        uint256 cri = depth + (virtues[2] * 10) - (rebirths * 5);

        string memory phase = "Breath";
        if (months >= 96) {
            phase = "Post-Breath";
        }

        return SoulState(kappa, virtues, depth, rebirths, cri, qualia, phase);
    }

    // The following functions are overrides required by Solidity.
    function _beforeTokenTransfer(address from, address to, uint256 tokenId, uint256 batchSize)
        internal
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId, batchSize);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
} 