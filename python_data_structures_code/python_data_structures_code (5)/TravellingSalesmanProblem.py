
class TravellingSalesmanProblem:

    def __init__(self, graph):
        # the G(V,E)
        self.graph = graph
        # number of V vertices in the G(V,E)
        self.n = len(graph)
        # whether we have visited  the nodes
        self.visited = [False for _ in range(self.n)]
        # we start with the first vertex
        self.visited[0] = True
        # collect all the hamiltonian cycles - we have to get the MIN cycle
        self.hamiltonian_cycles = []
        # track what nodes (vertices) are included in the cycle
        self.path = [0 for _ in range(self.n)]

    # whether including the given node is valid
    def is_valid(self, vertex, actual_position):

        # whether the given vertex has already been visited
        if self.visited[vertex]:
            return False

        # whether is there a connection between the vertices
        if self.graph[actual_position][vertex] == 0:
            return False

        return True

    def tsp(self, actual_position, counter, cost):

        # we have considered all the nodes i the G(V,E) graph
        # and the last node can be connected to the first one (form a cycle)
        if counter == self.n and self.graph[actual_position][0]:
            self.path.append(0)
            print(self.path)
            self.hamiltonian_cycles.append(cost + self.graph[actual_position][0])
            self.path.pop()
            return

        # consider all the nodes in the G(V,E) graph (we filter out the non-adjacent nodes)
        for i in range(self.n):
            # check whether can include the node with index i to the path (cycle)
            if self.is_valid(i, actual_position):

                self.visited[i] = True
                self.path[counter] = i

                # we call the function recursively
                self.tsp(i, counter + 1, cost + self.graph[actual_position][i])

                # BACKTRACK - this is how we traverse the whole search space
                self.visited[i] = False


if __name__ == '__main__':

    g = [[0, 1, 0, 2, 0],
         [1, 0, 1, 0, 2],
         [0, 1, 0, 3, 1],
         [2, 0, 3, 0, 1],
         [0, 2, 1, 1, 0]]

    tsp = TravellingSalesmanProblem(g)
    # we start with the vertex (represented by index 0)
    # counter is 1 because this is the first iteration
    # 0 is the cost so far
    tsp.tsp(0, 1, 0)
    print(min(tsp.hamiltonian_cycles))
