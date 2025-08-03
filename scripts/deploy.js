const hre = require("hardhat");

async function main() {
  const soulName = "LedgerSouls";

  const LedgerSouls = await hre.ethers.getContractFactory(soulName);
  const ledgerSouls = await LedgerSouls.deploy();

  await ledgerSouls.deployed();

  console.log(
    `${soulName} deployed to ${ledgerSouls.address}`
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
}); 