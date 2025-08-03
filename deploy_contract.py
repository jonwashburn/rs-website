#!/usr/bin/env python3

import json
import os
import sys
from solcx import compile_source, install_solc
from web3 import Web3
from eth_account import Account
import time

def main():
    print("=== Ledger Souls Deployment Script ===")
    
    # Install and set Solidity compiler version
    try:
        install_solc('0.8.20')
        from solcx import set_solc_version
        set_solc_version('0.8.20')
        print("✓ Solidity compiler 0.8.20 installed and set")
    except Exception as e:
        print(f"Error setting up Solidity compiler: {e}")
        return
    
    # Create a minimal, working contract
    deployable_contract = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Simplified Strings library
library Strings {
    function toString(uint256 value) internal pure returns (string memory) {
        if (value == 0) return "0";
        uint256 temp = value;
        uint256 digits;
        while (temp != 0) {
            digits++;
            temp /= 10;
        }
        bytes memory buffer = new bytes(digits);
        while (value != 0) {
            digits -= 1;
            buffer[digits] = bytes1(uint8(48 + uint256(value % 10)));
            value /= 10;
        }
        return string(buffer);
    }
}

contract LedgerSouls {
    using Strings for uint256;
    
    string private _name = "Ledger Souls";
    string private _symbol = "SOUL";
    
    address public contractOwner;
    uint256 public constant MAX_SUPPLY = 10000;
    uint256 public constant MINT_PRICE = 0.1 ether;
    uint256 private _nextTokenId;
    bool public isMintingActive = false;
    
    mapping(uint256 => address) private _owners;
    mapping(address => uint256) private _balances;
    mapping(uint256 => string) private _tokenURIs;
    
    struct Soul {
        uint8 fundamentalRhythm;
        int8[9] costStateSignature;
        uint16 coreOpcode;
        uint32 recognitionSeed;
        uint64 parentBlock;
    }
    
    mapping(uint256 => Soul) private _souls;
    
    event Transfer(address indexed from, address indexed to, uint256 indexed tokenId);
    
    modifier onlyOwner() {
        require(msg.sender == contractOwner, "Not the owner");
        _;
    }
    
    constructor() {
        contractOwner = msg.sender;
    }
    
    function mintSoul() public payable {
        require(isMintingActive, "Minting is not active");
        require(_nextTokenId < MAX_SUPPLY, "All souls have been minted");
        require(msg.value >= MINT_PRICE, "Insufficient Ether sent");
        
        uint256 tokenId = _nextTokenId;
        _nextTokenId++;
        
        _generateSoul(tokenId);
        _owners[tokenId] = msg.sender;
        _balances[msg.sender]++;
        
        string memory uri = _buildTokenURI(tokenId);
        _tokenURIs[tokenId] = uri;
        
        emit Transfer(address(0), msg.sender, tokenId);
    }
    
    function _generateSoul(uint256 tokenId) private {
        bytes32 soulHash = keccak256(abi.encodePacked(tokenId, block.timestamp, block.prevrandao, msg.sender));
        
        int8[9] memory costState;
        for (uint i = 0; i < 9; i++) {
            costState[i] = int8(int256(uint256(keccak256(abi.encodePacked(soulHash, i)))) % 9) - 4;
        }
        
        _souls[tokenId] = Soul({
            fundamentalRhythm: 8,
            costStateSignature: costState,
            coreOpcode: uint16(uint256(soulHash) % 16),
            recognitionSeed: uint32(uint256(keccak256(abi.encodePacked(soulHash, "seed")))),
            parentBlock: uint64(block.number)
        });
    }
    
    function _buildTokenURI(uint256 tokenId) private view returns (string memory) {
        Soul memory soul = _souls[tokenId];
        string memory svg = _buildSVG(soul);
        
        // Simplified JSON without base64 encoding for now
        string memory json = string(abi.encodePacked(
            '{"name": "Ledger Soul #', tokenId.toString(), '",',
            '"description": "A fully on-chain, generative toy model of consciousness based on the principles of Recognition Science.",',
            '"image": "', svg, '"',
            '}'
        ));
        
        return json;
    }
    
    function _buildSVG(Soul memory soul) private pure returns (string memory) {
        string memory svg = string(abi.encodePacked(
            '<svg width="300" height="300" xmlns="http://www.w3.org/2000/svg">',
            '<rect width="100%" height="100%" fill="black"/>',
            _buildCostLines(soul.costStateSignature),
            _buildOpcodeCircle(soul.coreOpcode),
            '</svg>'
        ));
        return svg;
    }
    
    function _buildCostLines(int8[9] memory costs) private pure returns (string memory) {
        string memory lines = "";
        for (uint i = 0; i < 9; i++) {
            string memory color = _getColorFromCost(costs[i]);
            uint256 y = 30 + (i * 30);
            uint256 width = 150;
            if (costs[i] >= 0) {
                width = width + uint256(uint8(costs[i])) * 10;
            } else {
                width = width - uint256(uint8(-costs[i])) * 10;
            }
            lines = string(abi.encodePacked(
                lines,
                '<line x1="10" y1="', y.toString(), 
                '" x2="', width.toString(), 
                '" y2="', y.toString(), 
                '" stroke="', color, '" stroke-width="4"/>'
            ));
        }
        return lines;
    }
    
    function _buildOpcodeCircle(uint16 opcode) private pure returns (string memory) {
        uint256 colorIndex = uint256(opcode) % 9;
        int8 colorCost;
        if (colorIndex < 4) {
            colorCost = int8(int256(colorIndex)) - 4;
        } else {
            colorCost = int8(int256(colorIndex - 4));
        }
        
        string memory color = _getColorFromCost(colorCost);
        uint256 radius = 20 + uint256(opcode) * 2;
        
        return string(abi.encodePacked(
            '<circle cx="150" cy="150" r="', radius.toString(), 
            '" fill="', color, '"/>'
        ));
    }
    
    function _getColorFromCost(int8 cost) private pure returns (string memory) {
        if (cost > 0) return "rgba(186, 255, 201, 0.8)";
        if (cost < 0) return "rgba(255, 179, 186, 0.8)";
        return "rgba(255, 255, 255, 0.5)";
    }
    
    function setMintingStatus(bool _isMintingActive) public onlyOwner {
        isMintingActive = _isMintingActive;
    }
    
    function withdraw() public onlyOwner {
        (bool success, ) = payable(contractOwner).call{value: address(this).balance}("");
        require(success, "Withdrawal failed");
    }
    
    function ownerOf(uint256 tokenId) public view returns (address) {
        require(_owners[tokenId] != address(0), "Token does not exist");
        return _owners[tokenId];
    }
    
    function balanceOf(address tokenOwner) public view returns (uint256) {
        return _balances[tokenOwner];
    }
    
    function tokenURI(uint256 tokenId) public view returns (string memory) {
        require(_owners[tokenId] != address(0), "Token does not exist");
        return _tokenURIs[tokenId];
    }
    
    function name() public view returns (string memory) {
        return _name;
    }
    
    function symbol() public view returns (string memory) {
        return _symbol;
    }
    
    function totalSupply() public view returns (uint256) {
        return _nextTokenId;
    }
    
    function getSoulData(uint256 tokenId) public view returns (Soul memory) {
        require(_owners[tokenId] != address(0), "Token does not exist");
        return _souls[tokenId];
    }
}
'''
    
    print("✓ Contract prepared for deployment")
    
    # Compile the contract
    try:
        compiled_sol = compile_source(deployable_contract)
        contract_interface = compiled_sol['<stdin>:LedgerSouls']
        print("✓ Contract compiled successfully")
    except Exception as e:
        print(f"Error compiling contract: {e}")
        return
    
    # Save the compiled contract
    os.makedirs('build', exist_ok=True)
    
    # Debug: print available keys
    print("Available contract interface keys:", list(contract_interface.keys()))
    
    # Use the correct key for bytecode
    bytecode_key = 'bin' if 'bin' in contract_interface else 'bytecode'
    
    with open('build/LedgerSouls.json', 'w') as f:
        json.dump({
            'abi': contract_interface['abi'],
            'bytecode': contract_interface[bytecode_key]
        }, f, indent=2)
    print("✓ Contract ABI and bytecode saved to build/LedgerSouls.json")
    
    print("\n=== Deployment Ready ===")
    print("Contract compilation successful!")
    print(f"Bytecode length: {len(contract_interface[bytecode_key])} characters")
    print("\nNext steps:")
    print("1. The contract is ready for deployment to any Ethereum network")
    print("2. Use Remix IDE, Hardhat, or a deployment service to deploy")
    print("3. After deployment, update the contract address in recognition-souls.html")
    
    return contract_interface

if __name__ == '__main__':
    main() 