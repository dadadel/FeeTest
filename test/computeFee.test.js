const { ethers } = require("hardhat");
const { expect } = require('chai');

describe("ComputeFeeTest", function () {
  let FeeComputation;
  let contract;
  const MAX_BALANCE = 1000000;
  const BALANCE_80p = 800000;
  const BALANCE_50p = 500000;

  beforeEach(async function () {
    FeeComputation = await ethers.getContractFactory("ComputeFeeTest");
    contract = await FeeComputation.deploy();
    await contract.deployed();
  });

  describe("Fee computation tests", function () {
    it("should return a fee of 0% when current balance is 100% of the maximum balance", async function () {
      expect(
        (await contract.computeFee(MAX_BALANCE)).toNumber()
      ).to.equal(0);
    });
    it("should return a fee of 1% when current balance is 80% of the maximum balance", async function () {
      expect(
        (await contract.computeFee(BALANCE_80p)).toNumber()
      ).to.equal(100);
    });
    it("should return a fee of 5% when current balance is 50% of the maximum balance", async function () {
      expect(
        (await contract.computeFee(BALANCE_50p)).toNumber()
      ).to.equal(500);
    });
    it("should return the fixed 5% fee for values under 50% of the balance", async function () {
      expect(
        (await contract.computeFee(BALANCE_50p - 1)).toNumber()
      ).to.equal(500);
      expect(
        (await contract.computeFee(BALANCE_50p - 100)).toNumber()
      ).to.equal(500);
      expect(
        (await contract.computeFee(1)).toNumber()
      ).to.equal(500);
    });
    it("should revert if balance is 0", async function () {
      await expect(
        contract.computeFee(0)
      ).to.be.revertedWith("Balance cannot be 0");
    });
    it("should revert if balance is over the maximum balance", async function () {
      await expect(
        contract.computeFee(MAX_BALANCE + 1)
      ).to.be.revertedWith("Balance exceeds maximum");
      await expect(
        contract.computeFee(MAX_BALANCE * 2)
      ).to.be.revertedWith("Balance exceeds maximum");
    });
  });
});
