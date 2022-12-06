import React, { useCallback, useEffect, useState } from "react";
import { useDropzone } from "react-dropzone";
import { ethers } from "ethers";
import IPFS from "ipfs";

import logo from "./ethereumLogo.png";
import { addresses, abis } from "@project/contracts";

import "./App.css";

const ZERO_ADDRESS =
  "0x0000000000000000000000000000000000000000000000000000000000000000";

let node;

const defaultProvider = new ethers.providers.Web3Provider(window.ethereum);

// IPFS hash storage contract
const ipfsContract = new ethers.Contract(
  addresses.ipfs,
  abis.ipfs,
  defaultProvider
);

// Oracle to model API contract
const oracleContract = new ethers.Contract(
  addresses.oracle,
  abis.oracle,
  defaultProvider
)

async function initIpfs() {
  node = await IPFS.create();
  const version = await node.version();
  console.log("IPFS Node Version:", version.version);
}

async function readCurrentUserFile() {
  const result = await ipfsContract.fileHashes(
    defaultProvider.getSigner().getAddress()
  );
  console.log({ result });

  return result;
}

function App() {
  const [ipfsHash, setIpfsHash] = useState("");
  useEffect(() => {
    initIpfs();
    window.ethereum.enable();
  }, []);

  useEffect(() => {
    async function readFile() {
      const file = await readCurrentUserFile();

      if (file !== ZERO_ADDRESS) setIpfsHash(file);
    }
    readFile();
  }, []);

  // Convert file to base64 for GET request
  const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = error => reject(error);
  });

  // Store ipfs hash in storage smart contract
  async function setFile(hash) {
    const ipfsWithSigner = ipfsContract.connect(defaultProvider.getSigner());
    const tx = await ipfsWithSigner.storeImageHash(hash);
    console.log({ tx });

    setIpfsHash(hash);
  }

  // Upload file to IPFS if deemed valid by deepfake model
  const uploadFile = useCallback(async (file) => {
    // DEBUG
    // const buffer = await file.arrayBuffer();
    // let byteArray = new Int8Array(buffer);
    // console.log(buffer);
    // console.log(byteArray);
    console.log(await toBase64(file));

    let url = "http://localhost:8000/"
    let path = await toBase64(file)

    const oracleWithSigner = oracleContract.connect(defaultProvider.getSigner());
    const tx = await oracleWithSigner.requestConfidenceScore(url, path);
    console.log({ tx });

    // DEBUG
    // fetch(`${url}?path=${path}`);
    

    const files = [
      {
        path: file.name + file.path,
        content: file,
      },
    ];

    for await (const result of node.add(files)) {
      await setFile(result.cid.string);
    }
  }, []);

  const onDrop = useCallback(
    (acceptedFiles) => {
      uploadFile(acceptedFiles[0]);
    },
    [uploadFile]
  );
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    multiple: false,
    onDrop,
  });

  return (
    <div className="App">
      <header className="App-header">
        <div {...getRootProps()} style={{ cursor: "pointer" }}>
          <img src={logo} className="App-logo" alt="react-logo" />
          <input {...getInputProps()} />
          {isDragActive ? (
            <p>Drop the files here ...</p>
          ) : (
            <p>
              Drag 'n' drop some files here to validate an image (or click the
              logo)
            </p>
          )}
        </div>
        <div>
          {ipfsHash !== "" ? (
            <a
              href={`https://ipfs.io/ipfs/${ipfsHash}`}
              target="_blank"
              rel="noopener noreferrer"
            >
              See current user file
            </a>
          ) : (
            "No file submitted yet..."
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
