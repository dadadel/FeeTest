#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt

# not exactly the limits but good enough!
MAX_INT128 = int(1.7e38)
MIN_INT128 = int(-1.7e38)
MAX_INT256 = int(5.7e76)
MIN_INT256 = int(-5.7e76)

BPS_100p = 10000
BPS_1p = 100
BPS_5p = 500

MAX_USDT = 1000000
MAX_USDT_50 = MAX_USDT // 2
MAX_USDT_80 = MAX_USDT*80 // 100


def compute_coefs(points):
    (x1, y1), (x2, y2), (x3, y3) = points
    coefs = np.polyfit((x1, x2, x3), (y1, y2, y3), 2)
    return coefs

def check_overflow(x):
#    assert MIN_INT256 <= x <= MAX_INT256
    assert MIN_INT128 <= x <= MAX_INT128


def compute_poly(x, a, b, c):
    check_overflow(a*x*x)
    check_overflow(b*x)
    y = a*x*x + b*x + c
    check_overflow(y)
    return y


def compute_fee(balance, coefs, coefmult):
    a, b, c = coefs
    assert balance <= MAX_USDT
    if balance < MAX_USDT_50:
        fee = BPS_5p
    elif balance >= MAX_USDT:
        fee = 0
    else:
        fee = compute_poly(balance, a, b, c) // coefmult if coefmult else compute_poly(balance, a, b, c)
    return fee


def plot_2nd(x, y, coefs, coefmult):
    plt.title(f"y = ({coefs[0]}*x^2+{coefs[1]}*x+{coefs[2]})/{coefmult}") 
    plt.xlabel(r"balance") 
    plt.ylabel(r"fee %") 
    plt.plot(x,y) 
    plt.show()

if __name__ == "__main__":
    points = (MAX_USDT, 0), (MAX_USDT_80, BPS_1p), (MAX_USDT_50, BPS_5p)
    coefs = compute_coefs(points)
    coefmult = int(1e25)
    coefs = int(coefs[0] * coefmult), int(coefs[1] * coefmult), int(coefs[2] * coefmult)
    prev = None
    count = 0
    under = 0
    x = []
    y = []
    for i in range(MAX_USDT_50+1):
        f = compute_fee(MAX_USDT-i, coefs, coefmult)
        if f != prev:
            x.append(MAX_USDT-i)
            y.append(f/100)
            print(MAX_USDT-i,f)
            count += 1
            prev = f
        if f < 0:
            under += 1
    print("count of different fee values:", count)
    print("count of fees under 0:", under)
    print("Coefs:", ", ".join(str(c) for c in coefs))
    print("Coef correction number:", coefmult)
    print("Fee for 100%:", compute_fee(MAX_USDT, coefs, coefmult))
    print("Fee for 80%:", compute_fee(MAX_USDT_80, coefs, coefmult))
    print("Fee for 50%:", compute_fee(MAX_USDT_50, coefs, coefmult))
    plot_2nd(x, y, coefs, coefmult)
