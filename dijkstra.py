from __future__ import annotations

import heapq
import sys

from typing import Any


class Vertex:
    '''
    Vertex represents a node of a graph. 
    It has all adjacent neighbor nodes as a dictionary, 
    and other information such as distance, whether it's visited or not, and a pointer to previous node.
    '''

    def __init__(self, id: str):
        self.__id: str = id

        # keeps all the neighbor Vertices
        self.__adjacent: dict[Vertex, float] = {}

        # Distance from the start Vertex to current Vertex
        # Set distance to infinity for all nodes
        self.__distance: float = float('inf')

        # Mark all nodes unvisited
        self.__visited: bool = False

        # Predecessor for tracking a path down
        self.__previous: Vertex = None

    @property
    def id(self) -> str:
        ''' getter for id '''
        return self.__id

    @id.setter
    def id(self, id: str):
        ''' setter for id '''
        self.__id = id

    @property
    def distance(self) -> float:
        ''' getter for distance '''
        return self.__distance

    @distance.setter
    def distance(self, distance: float):
        ''' setter for distance '''
        self.__distance = distance

    @property
    def visited(self) -> bool:
        ''' getter for visited '''
        return self.__visited

    @visited.setter
    def visited(self, visited: bool):
        ''' setter for visited '''
        self.__visited = visited

    @property
    def previous(self) -> Vertex:
        ''' getter for previous '''
        return self.__previous

    @previous.setter
    def previous(self, previous: Vertex):
        ''' setter for previous '''
        self.__previous = previous

    def add_neighbor(self, neighbor: Vertex, weight: float = 0) -> None:
        ''' add a neighbor Vertex '''
        self.__adjacent[neighbor] = weight

    def neighbors(self) -> list[Vertex]:
        ''' get a list of neighbor Vertices '''
        return self.__adjacent.keys()

    def weight_to(self, neighbor: Vertex) -> float:
        ''' get weight between self and neighbor Vertex '''
        return self.__adjacent[neighbor]

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.distance == other.distance

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.distance < other.distance

    def __gt__(self, other: Any) -> bool:
        if not isinstance(other, Vertex):
            return NotImplemented
        return self.distance > other.distance

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        adjacent = str(
            [f'{x.id}({x.distance}, Visited:{x.visited})' for x in self.__adjacent])
        return f'id: {self.id}({self.distance}), adjacent: {adjacent}'

    def __repr__(self):
        if self.visited:
            return f'({self.id},{self.distance})'
        else:
            return f'[{self.id},{self.distance}]'


class Graph:
    ''' Graph represents vertices and edges '''

    def __init__(self):
        self.__vertices: Dict[str: Vertex] = {}

    def __iter__(self):
        return iter(self.__vertices.values())

    def size(self) -> int:
        ''' return the number of vertices '''
        return len(self.__vertices)

    def add_vertex(self, id: str):
        ''' add a vertex '''
        self.__vertices[id] = Vertex(id)

    def get_vertex(self, id: str) -> Vertex:
        ''' get vertex by id '''
        if id in self.__vertices:
            return self.__vertices[id]
        else:
            return None

    def add_edge(self, from_id: str, to_id: str, weight: float = 0):
        ''' add edge between two vertices '''

        # add vertex if its id is not in the graph
        if from_id not in self.__vertices:
            self.add_vertex(from_id)
        if to_id not in self.__vertices:
            self.add_vertex(to_id)

        # no direction between two vertices, so add each other to its neighbor
        self.__vertices[from_id].add_neighbor(self.__vertices[to_id], weight)
        self.__vertices[to_id].add_neighbor(self.__vertices[from_id], weight)

    def vertices(self) -> list[Vertex]:
        ''' get all the vertices in the graph '''
        return list(self.__vertices.values())

    def __str__(self):
        print('Graph data:')
        items = []
        for current in self.__vertices.values():
            for neighbor in current.neighbors():
                items.append(
                    f'({current.id}, {neighbor.id}, {current.weight_to(neighbor)})')

        output = '\n'.join(items)
        return output


def dijkstra(graph, s_vertex, e_vertex):
    ''' dijkstra algorithm '''
    print("Dijkstra's shortest path")

    # set the distance for the start node to zero
    s_vertex.distance = 0

    unvisited = graph.vertices()
    # priority queue, https://docs.python.org/3/library/heapq.html
    heapq.heapify(unvisited)

    while len(unvisited):
        # pops a vertex with the smallest distance
        current = heapq.heappop(unvisited)
        print(f'[Current Vertex] {current}')
        current.visited = True

        for neighbor in current.neighbors():
            # if visited, skip
            if neighbor.visited:
                print(f'\t{neighbor.id} is already visited.')
                continue

            distance_to_neighbor = current.distance + \
                current.weight_to(neighbor)

            # if it's better, update information of the neighbor Vertex
            neighbor_prev_distance = neighbor.distance
            if distance_to_neighbor < neighbor_prev_distance:
                neighbor.distance = distance_to_neighbor
                neighbor.previous = current
                print(
                    f'\t{neighbor.id}(weight between:{current.weight_to(neighbor)}) is updated (from: {neighbor_prev_distance} to {neighbor.distance})')
            else:
                print(
                    f'\t{neighbor.id}(weight between:{current.weight_to(neighbor)}) is not updated (still {neighbor_prev_distance})')

        # rebuild heap
        # 1. pop every item
        while len(unvisited):
            heapq.heappop(unvisited)
        # 2. put all vertices not visited into the queue
        unvisited = [v for v in graph.vertices() if not v.visited]
        heapq.heapify(unvisited)
        print()


def shortest(v):
    ''' make shortest path from v.previous'''
    path = [v]
    p = v.previous
    while p:
        path.append(p)
        p = p.previous
    return path


if __name__ == '__main__':

    g = Graph()

    # example 1, build a graph
    g.add_edge('a', 'b', 7)
    g.add_edge('a', 'c', 9)
    g.add_edge('a', 'f', 14)
    g.add_edge('b', 'c', 10)
    g.add_edge('b', 'd', 15)
    g.add_edge('c', 'd', 11)
    g.add_edge('c', 'f', 2)
    g.add_edge('d', 'e', 6)
    g.add_edge('e', 'f', 9)

    # example 2, build a graph
    # g.add_edge('a', 'b', 12)
    # g.add_edge('a', 'f', 16)
    # g.add_edge('a', 'g', 14)
    # g.add_edge('b', 'c', 10)
    # g.add_edge('b', 'f', 7)
    # g.add_edge('g', 'f', 9)
    # g.add_edge('g', 'e', 8)
    # g.add_edge('f', 'c', 6)
    # g.add_edge('f', 'e', 2)
    # g.add_edge('c', 'e', 5)
    # g.add_edge('c', 'd', 3)
    # g.add_edge('e', 'd', 4)

    print(g)

    # set start, end vertex
    start_vertex = g.get_vertex('a')
    end_vertex = g.get_vertex('d')

    # update distance of all the vertices in the graph using dijkstra algorithm
    dijkstra(g, start_vertex, end_vertex)

    # find shortest path
    path = shortest(end_vertex)
    print(f'The shortest path: {path[::-1]}')
