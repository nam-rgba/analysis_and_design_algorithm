package Lab06;

public class Lab06 {
    public static int binomialCoefficient(int n, int k) {
        int[][] dp = new int[n + 1][k + 1];

        for (int i = 0; i <= n; i++) {
            dp[i][0] = 1;
        }
        for (int j = 0; j <= k; j++) {
            dp[j][j] = 1;
        }

        for (int i = 1; i <= n; i++) {
            for (int j = 1; j <= Math.min(i, k); j++) {
                dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j];
            }
        }
        return dp[n][k];
    }
    // Analysis:
    // Basic:line 11
    // Worst case: There is no worst case
    // The total number of basic operation is: T(n,k)=(n-1)*(k)
    // Time complexility: O(nk)

    public static int coinRow(int[] coins) {
        int n = coins.length;

        if (n == 0) {
            return 0;
        } else if (n == 1) {
            return coins[0];
        }

        // Store maximum value of each position
        int[] dp = new int[n];

        // base
        dp[0] = coins[0];
        dp[1] = Math.max(coins[0], coins[1]);

        for (int i = 2; i < n; i++) {
            dp[i] = Math.max(dp[i - 1], dp[i - 2] + coins[i]);
        }

        return dp[n - 1];

    }
    // Analysis:
    // Basic:line 30
    // Worst case: fill in every entry in the table
    // The total number of basic operation is: T(n)=n-2
    // Time complexility: O(n)

    public static int minCoin(int[] coins, int amount) {
        int dp[] = new int[amount + 1];

        // Initialize the dp array with a value higher than any possible solution
        for (int i = 1; i <= amount; i++) {
            dp[i] = Integer.MAX_VALUE;
        }

        // Fill in the dp array using the recurrence relation
        for (int coin : coins) {
            for (int i = coin; i <= amount; i++) {
                if (dp[i - coin] != Integer.MAX_VALUE) {
                    dp[i] = Math.min(dp[i], dp[i - coin] + 1);
                }
            }
        }

        // The result is the value at the last position of the dp array
        return dp[amount] == Integer.MAX_VALUE ? -1 : dp[amount];
    }

    // Analysis:
    // Basic:line 67
    // Worst case:no worst case
    // The total number of basic operation is: T(n, a)=a*n
    // Time complexility: O(n*amount)

    public static int knapsack(int[] weights, int[] values, int capacity) {
        int n = weights.length;

        // dp[i][j] represents the maximum value that can be achieved with a knapsack
        // using the first i items.
        int[][] dp = new int[n + 1][capacity + 1];

        // Build the dp table using the recurrence relation
        for (int i = 1; i <= n; i++) {
            for (int j = 0; j <= capacity; j++) {
                // skip
                if (weights[i - 1] > j) {
                    dp[i][j] = dp[i - 1][j];
                } else {
                    // Choose the maximum value
                    dp[i][j] = Math.max(dp[i - 1][j], values[i - 1] + dp[i - 1][j - weights[i - 1]]);
                }
            }
        }

        // The result is in the bottom-right
        return dp[n][capacity];
    }
    // Analysis:
    // Basic:line 95
    // Worst case: fill in the entire 2D array dp for all possible subproblems.
    // The total number of basic operation is: T(n, capacity)=c×(n+1)×(capacity+1)
    // Time complexility: O(n*capacity)

    public static void main(String[] args) {
        int n = 5;
        int k = 2;
        int result = binomialCoefficient(n, k);
        System.out.println("C(" + n + ", " + k + ") = " + result);

        int[] coins = { 2, 4, 1, 2, 7, 8 };
        int contMaxs = coinRow(coins);
        System.out.println("Maximum coin value: " + contMaxs);

        int amount = 11;
        int mincoint = minCoin(coins, amount);
        System.out.println("Minimum number of coins to make change: " + mincoint);

        int[] weights = { 2, 3, 4, 5 };
        int[] values = { 3, 4, 5, 6 };
        int capacity = 5;

        int maxValue = knapsack(weights, values, capacity);
        System.out.println("Maximum value in the knapsack: " + maxValue);
    }
}
