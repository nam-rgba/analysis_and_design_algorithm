
def binomial_coefficient(n, k):
    # Base cases
    if k == 0 or k == n:
        return 1

    # Divide: C(n, k) = C(n-1, k-1) + C(n-1, k)
    left = binomial_coefficient(n - 1, k - 1)
    right = binomial_coefficient(n - 1, k)

    # Conquer: Combine the solutions
    return left + right

def max_coin_value(coins):
    n = len(coins)

    if n == 0:
        return 0
    elif n == 1:
        return coins[0]

    # Divide: Choose the first coin or skip it
    include_first = coins[0] + max_coin_value(coins[2:])
    exclude_first = max_coin_value(coins[1:])

    # Conquer: Return the maximum value
    return max(include_first, exclude_first)


def min_coins(coins, amount):
    if amount == 0:
        return 0
    if amount < 0:
        return float('inf')

    min_count = float('inf')

    for coin in coins:
        subproblem = 1 + min_coins(coins, amount - coin)
        min_count = min(min_count, subproblem)

    return min_count

import time

def measure_time(func, N):
    runtime=[]
    
    for n in N:
        start=time.time()
        f=func(n)
        stop=time.time()
        runtime.append(stop-start)
    return runtime

import pylab

# result = binomial_coefficient(n, k)
N=[[5,2],[6,4],[3,2]]
rtime=measure_time(binomial_coefficient, N)

M=[
    [2, 4, 1, 2, 7, 8],
    [2, 4, 1, 2, 7, 8,3,23,3],
    [2, 4, 1, 2, 7, 8,2,1,3,4,1,2,1],
    [2, 4, 1, 2, 7, 8,1,3,1,5,7,8,1,8,4]
]
# rtime2=measure_time(max_coin_value,[M])
# pylab.plot(N, rtime)
# pylab.legend(['binomial_coefficient'])
# pylab.show()