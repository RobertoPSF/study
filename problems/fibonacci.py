#reccursive
def fib(n):
    if n <= 2:
        return n
    return fib(n - 1) + fib(n - 2)

#reccursive with memoization
def fib(n):
    memo = {}

    def dp(k):
        if k <= 2:
            return k
        if k in memo:
            return memo[k]

        memo[k] = dp(k - 1) + dp(k - 2)
        return memo[k]

    return dp(n)

#dp
def fib(n):
    if n <= 2:
        return n

    dp = [0] * (n + 1)
    dp[1] = 1
    dp[2] = 2

    for i in range(3, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]

    return dp[n]