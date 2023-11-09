package Lab05;

import java.util.Random;

public class Lab05 {

    public static void recursiveInsertionSort(int[] arr, int n) {
        if (n <= 1) {
            return;
        }

        // Sort the first (n-1) elements recursively
        recursiveInsertionSort(arr, n - 1);

        // Insert the nth element into the sorted subarray
        int lastElement = arr[n - 1];
        int j = n - 2;

        // Shift elements of the sorted subarray that are greater than lastElement
        while (j >= 0 && arr[j] > lastElement) {
            arr[j + 1] = arr[j];
            j--;
        }

        // Insert lastElement in its correct position
        arr[j + 1] = lastElement;
    }
    // Analysis
    // Basic:n==1
    // Worst case: input array is in descending order
    // The total number of basic operation is: T(n)=T(n-1)
    // So the complexity ot the algorithms is O(n)

    /*-------------------------------------------------------------------------------------------------------- */

    public static double power(double base, int exponent) {

        if (exponent == 0) {
            return 1;
        }

        // Recursive case: Calculate the result for a smaller exponent.
        if (exponent > 0) {
            return base * power(base, exponent - 1);
        } else {
            // If the exponent is negative, invert the base and make the exponent positive.
            base = 1 / base;
            exponent = -exponent;
            return base * power(base, exponent - 1);
        }
    }

    // Analysis
    // Basic:exponent=0
    // Worst case: no worst case
    // The total number of basic operation is: T(1)
    // So the complexity ot the algorithms is O(1)
    /*-------------------------------------------------------------------------------------------------------- */

    public static int euclideanGCD(int a, int b) {

        if (b == 0) {
            return a;
        } else {
            return euclideanGCD(b, a % b);
        }
    }

    // Analysis
    // Basic:b==0
    // Worst case: no worst case
    // The total number of basic operation is: T(1)
    // So the complexity ot the algorithms is O(1)
    /*-------------------------------------------------------------------------------------------------------- */

    public static int quickSelect(int[] arr, int left, int right, int k) {
        if (left == right) {
            return arr[left];
        }

        int pivotIndex = partition(arr, left, right);

        if (k == pivotIndex) {
            return arr[pivotIndex];
        } else if (k < pivotIndex) {
            return quickSelect(arr, left, pivotIndex - 1, k);
        } else {
            return quickSelect(arr, pivotIndex + 1, right, k);
        }
    }

    private static int partition(int[] arr, int left, int right) {
        int pivotIndex = choosePivot(left, right);
        int pivotValue = arr[pivotIndex];
        swap(arr, pivotIndex, right);

        int storeIndex = left;
        for (int i = left; i < right; i++) {
            if (arr[i] < pivotValue) {
                swap(arr, storeIndex, i);
                storeIndex++;
            }
        }
        swap(arr, storeIndex, right);
        return storeIndex;
    }

    // Analysis
    // Worst case: when poorly chosen pivots are consistently selected
    // The total number of basic operation is: T(n^2)
    // So the complexity ot the algorithms is O(n^2)
    /*-------------------------------------------------------------------------------------------------------- */

    private static int choosePivot(int left, int right) {
        // In this example, we'll choose a random pivot.
        Random rand = new Random();
        return left + rand.nextInt(right - left + 1);
    }

    private static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    public static void main(String[] args) {
        int[] arr = { 12, 11, 13, 5, 6 };
        int n = arr.length;

        System.out.println("Unsorted array:");
        for (int value : arr) {
            System.out.print(value + " ");
        }

        recursiveInsertionSort(arr, n);

        System.out.println("\nSorted array:");
        for (int value : arr) {
            System.out.print(value + " ");
        }

        int num1 = 48;
        int num2 = 18;

        int gcd = euclideanGCD(num1, num2);
        System.out.println("GCD of " + num1 + " and " + num2 + " is: " + gcd);

        double base = 2.0;
        int exponent = 5;

        double result2 = power(base, exponent);
        System.out.println(base + " ^ " + exponent + " = " + result2);

        // Graph graph = new Graph(7);
        // graph.addEdge(0, 1);
        // graph.addEdge(0, 2);
        // graph.addEdge(1, 3);
        // graph.addEdge(1, 4);
        // graph.addEdge(2, 5);
        // graph.addEdge(2, 6);

        // System.out.print("DFS starting from vertex 0: ");
        // graph.depthFirstSearch(0);

        int k = 2;
        int result6 = quickSelect(arr, 0, arr.length - 1, k);
        System.out.println("The " + (k + 1) + "-th smallest element is: " + result6);
    }

}
