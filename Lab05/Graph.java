package Lab05;

import java.util.ArrayList;
import java.util.List;

public class Graph {
    private int vertices;
    private List<List<Integer>> adjList;

    public Graph(int vertices) {
        this.vertices = vertices;
        adjList = new ArrayList<>(vertices);
        for (int i = 0; i < vertices; i++) {
            adjList.add(new ArrayList<>());
        }
    }

    public void addEdge(int source, int destination) {
        adjList.get(source).add(destination);
    }

    public void dfs(int vertex, boolean[] visited) {
        visited[vertex] = true;
        System.out.print(vertex + " ");

        for (Integer neighbor : adjList.get(vertex)) {
            if (!visited[neighbor]) {
                dfs(neighbor, visited);
            }
        }
    }

    public void depthFirstSearch(int startVertex) {
        boolean[] visited = new boolean[vertices];
        dfs(startVertex, visited);
    }
}
// Analysis
// Basic: on line 27
// Worst case: visit all the vertices and edges of the graph
// The total number of basic operation is: T(V+E)
// So the complexity ot the algorithms is O(V+E)
/*-------------------------------------------------------------------------------------------------------- */