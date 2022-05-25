pragma solidity ^0.8.13;

contract ComputeFeeTest {
    uint256 private constant MAX_BALANCE = 1000000;
    uint256 private constant MAX_BALANCE_50 = MAX_BALANCE / 2;
    uint256 private constant BPS_100p = 10000;
    uint256 private constant BPS_5p = 500;

    /**
     * Compute the 2nd degree polynomial
     */
    function _computePoly2(int256 _x) internal pure returns(int256 y) {
        // the coeffifients values and the following division is to keep the
        // coefficients in integer domain and thus avoid usage of fixed point
        y = 16666666666666480 * _x**2 - 34999999999999863685120 * _x + 18333333333333350527742771200;
        y /= 1e25;
    }

    /**
     * Compute the fee based on the given balance
     * @param _balance the balance to compute the fee for
     * @return fee the computed amount of fee to pay
     */
    function computeFee(uint256 _balance) external pure returns(uint256 fee) {
        require(_balance > 0, "Balance cannot be 0");
        require(_balance <= MAX_BALANCE, "Balance exceeds maximum");

        if(_balance <= MAX_BALANCE_50) {
            fee = BPS_5p;
        }
        else if(_balance == MAX_BALANCE) {
            fee = 0;
        }
        else {
            fee = uint256(_computePoly2(int256(_balance)));
        }
    }
}
