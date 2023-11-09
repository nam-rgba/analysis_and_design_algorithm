package Lab04;

import java.util.ArrayList;

class Program {

    public class Node {
        int value;
        Node left, right;

        public Node(int item) {
            value = item;
            left = right = null;
        }
    }

    Node root = new Node(0);

    // Exercies 1
    public static int binarySearch(int[] arr, int target) {
        int left = 0;
        int right = arr.length - 1;

        while (left <= right) {
            int mid = left + (right - left) / 2;

            if (arr[mid] == target) {
                return mid;
            } else if (arr[mid] < target) {
                left = mid + 1;
            } else {
                right = mid - 1;
            }
        }

        return -1;
    }
    // Basic on line 11
    // The worst case is target in the end of array
    // T(n)=n
    // O(n)
    /*----------------------------------------------------------------------------------------------------------- */

    // Exercise 2
    static void swap(int[] arr, int i, int j) {
        int temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }

    static int partition(int[] arr, int high, int low) {
        int pivot = arr[high];
        int i = low - 1;
        for (int j = low; j <= high - 1; j++) {
            if (arr[j] < pivot) {
                i++;
                swap(arr, i, j);
            }
        }
        swap(arr, i + 1, high);
        return (i + 1);
    }

    static void quickSort(int[] arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quickSort(arr, low, pi - 1);
            quickSort(arr, pi + 1, high);
        }
    }

    // Basic on line 48
    // Worst case is array was sorted
    // T(n)=nlogn (avarage)
    // O(nlogn) in average case, O(n^2) in worst case
    /*----------------------------------------------------------------------------------------------------------- */

    // Exercise 3

    int maxDepth(Node node) {
        if (node == null)
            return 0;
        else {

            int lDepth = maxDepth(node.left);
            int rDepth = maxDepth(node.right);

            if (lDepth > rDepth)
                return (lDepth + 1);
            else
                return (rDepth + 1);
        }
    }
    // Basic on line 72
    // No worst case
    // T(n)=n
    // O(n)
    /*----------------------------------------------------------------------------------------------------------- */

    // Exercise 4
    // Pre oder
    public ArrayList<Integer> preOder(Node root) {
        ArrayList<Integer> result = new ArrayList<Integer>();
        if (root == null) {
            return result;
        }
        result.add(root.value);
        ArrayList<Integer> leftResult = preOder(root.left);
        if (leftResult.size() > 0) {
            result.addAll(leftResult);
        }

        ArrayList<Integer> rightResult = preOder(root.right);
        if (rightResult.size() > 0) {
            result.addAll(rightResult);
        }

        return result;
    }

    // In oder
    public ArrayList<Integer> inOder(Node root) {
        ArrayList<Integer> result = new ArrayList<Integer>();
        if (root == null) {
            return result;
        }
        ArrayList<Integer> leftResult = inOder(root.left);
        if (leftResult.size() > 0) {
            result.addAll(leftResult);
        }
        result.add(root.value);

        ArrayList<Integer> rightResult = inOder(root.right);
        if (rightResult.size() > 0) {
            result.addAll(rightResult);
        }

        return result;
    }

    public ArrayList<Integer> postOder(Node root) {
        ArrayList<Integer> result = new ArrayList<Integer>();
        if (root == null) {
            return result;
        }
        ArrayList<Integer> leftResult = postOder(root.left);
        if (leftResult.size() > 0) {
            result.addAll(leftResult);
        }

        ArrayList<Integer> rightResult = postOder(root.right);
        if (rightResult.size() > 0) {
            result.addAll(rightResult);
        }
        result.add(root.value);

        return result;
    }

    // Analysis
    // Basic:node==null
    // Worst case: The worst case is the average case too, because the algorithm
    // runs the same in all situations.
    // The total number of basic operation is: Max of edge is n-1, where n is total
    // of nodes => T(n)=T(n+n-1)
    // So the complexity ot the algorithms is O(n)

    /*-------------------------------------------------------------------------------------------------------- */

    // Exercise 5
    // class Point {
    // public int x, y;

    // Point(int x, int y) {
    // this.x = x;
    // this.y = y;
    // }

    // // Distance between 2 points
    // public static float dist(Point p1, Point p2) {
    // return (float) Math.sqrt((p1.x - p2.x) * (p1.x - p2.x) + (p1.y - p2.y) *
    // (p1.y - p2.y));
    // }

    // }

    public static void main(String[] args) {

    }

}