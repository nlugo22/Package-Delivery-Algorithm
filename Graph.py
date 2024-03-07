from HashTable import ChainingHashTable
class Vertex:
    def __init__(self, id, label):
        self.label = label
        self.id = id
        self.distance = float('inf')
        self.pred_vertex = None


class Graph:
    def __init__(self):
        self.vertexHash = ChainingHashTable()
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

# take the data in from the distance table

    def makeGraph(self, g, addressList, distanceList):

        # count is used for the id to store vertexes in a hashtable
        count = 0
        for item in addressList:
            v = Vertex(count, item)
            g.add_vertex(v)
            # add into the hashtable
            self.vertexHash.insert(count, v)
            # update count for next loop
            count += 1

        # Add edges based on distanceList
        for i in range(len(addressList)):
            for j in range(i, len(addressList)):

                edge_distance = float(distanceList[j][i])

                if edge_distance != '':
                    vertex_a = self.vertexHash.search(i)
                    vertex_b = self.vertexHash.search(j)
                    g.add_undirected_edge(vertex_a, vertex_b, edge_distance)

        return g



