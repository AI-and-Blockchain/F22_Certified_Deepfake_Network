pragma solidity ^0.6.11;

contract StorageTest {
    mapping (string => string) public fileHashes;

    function storeImageHash (string memory file) external {
        fileHashes[file] = file;
    }
}