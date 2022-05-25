pragma solidity ^0.8.13;

contract ComputeFeeTest {
    uint256 private constant MAX_BALANCE = 1000000;
    uint256 private constant MAX_BALANCE_50 = MAX_BALANCE / 2;
    uint256 private constant BPS_100p = 100000000;
    uint256 private constant BPS_5p = 5000000;

    /**
     * Compute the 2nd degree polynomial
     */
    function _computePoly2(int256 _x) internal pure returns(int256 y) {
        // the coeffifients values and the following division is to keep the
        // coefficients in integer domain and thus avoid usage of fixed point
        y = 1666666666666646 * _x**2 - 3499999999999984271360 * _x + 1833333333333334228140556288;
        y /= 1e20;
    }

    /**
     * Compute the fee based on the given balance
     * @param _balance the balance to compute the fee for
     * @return fee the computed amount of fee to pay
     */
    function computeFee(uint256 _balance) external pure returns(uint256 fee) {
        require(_balance > 0, "Balance cannot be 0");
        require(_balance < MAX_BALANCE, "Balance exceeds maximum allowed");

        if(_balance <= MAX_BALANCE_50) {
            fee = BPS_5p;
        }
        else {
            fee = uint256(_computePoly2(int256(_balance)));
        }
    }
}
