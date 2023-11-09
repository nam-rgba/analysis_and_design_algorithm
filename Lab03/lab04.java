import java.lang.Math;
import java.lang.reflect.Array;

public class lab04 {
    static int exponentialPower(int a, int n) {
        // n, a : input value
        // result: out put a^n
        int result = 1;
        while (n > 0) {
            result = result * a;
            n--;
        }
        return result;
    }
    // Analysis
    /*
     * + Basic on line 14
     * + No worst case
     * + T(n)=n
     * + O(n)
     */
    /*
     * -----------------------------------------------------------------------------
     * ---------------------------
     */

    static int factorial(int n) {
        int r = 1;
        for (int i = 1; i < n; i++) {
            r *= i;
        }
        return r;
    }

    static int combination(int n, int k) {
        // n, k : input value
        return (factorial(n) / (factorial(k) * factorial(n - k)));
    }

    // Analysis
    /*
     * + Basic on line 32
     * + No worst case
     * + T(n)=n
     * + O(n)
     */
    /*
     * -----------------------------------------------------------------------------
     * ---------------------------
     */
    static int[][] matrix(int[][] a, int[][] b, int n) {
        int c[][] = new int[n][n];
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                for (int k = 0; k < n; k++) {
                    c[i][j] = a[i][k] * b[k][j];
                }
            }
        }
        return c;
    }
    // Analysis
    /*
     * + Basic :i,j=n-1
     * + No worst case
     * + T(n)=n^3
     * + O(n^3)
     */
    /*
     * -----------------------------------------------------------------------------
     * ---------------------------
     */

    static double pair(double a[], double b[], int d) {
        // a, b: input value
        // d: length of input
        double r = 0;
        for (int i = 0; i < d; i++) {
            r += (a[i] * a[i] - b[i] * b[i]) * (a[i] * a[i] - b[i] * b[i]);
        }
        return Math.sqrt(r);
    }

    static double closetPair(double points[][], int n) {
        // points: input value
        // n: length of input
        // min: result-closest distance
        double min = pair(points[0], points[1], points[0].length);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                if (i != j) {
                    if (min < pair(points[i], points[j], points[0].length)) {
                        min = pair(points[i], points[j], points[0].length);

                    }
                }
            }
        }
        return min;
    }

    // Analysis
    /*
     * + Basic :i,j=n-1
     * + Worst case: 2 closest pair in the last of array
     * + T(n)=n^2*d
     * + O(n^2)
     */
    /*
     * -----------------------------------------------------------------------------
     * ---------------------------
     */

    public static void main(String[] args) {
        int a = 4, n = 5;
        int[][] mtx1 = { { 1, 3, 5 }, { 2, 6, 3 }, { 4, 9, 7 } };
        int[][] mtx2 = { { 1, 3, 6 }, { 1, 5, 3 }, { 0, 3, 7 } };
        double[][] points = { { 1, 3, 6, 3, 7 }, { 2, 3, 7, 4, 6 }, { 9, 9, 9, 9, 9 }, { 5, 6, 3, 6, 8 } };

        int exca = exponentialPower(a, n);
        System.out.println(exca);
        int excb = factorial(n);
        System.out.println(excb);
        double excd = closetPair(points, 4);
        System.out.println(excd);

    }
}