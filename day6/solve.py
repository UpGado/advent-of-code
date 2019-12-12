from collections import defaultdict, deque, namedtuple
from pprint import pprint

Planet = namedtuple('Planet', 'orbits orbited_by')


def parse_orbit(orbit_str):
    return tuple(orbit_str.split(')'))


def build_graph(orbits):
    graph = defaultdict(lambda: Planet(set(), set()))
    for center, satelite in orbits:
        graph[center].orbited_by.add(satelite)
        graph[satelite].orbits.add(center)
    return graph


def traverse_graph(graph, origin, process_func, order='bfs', directed=True):
    node_vals = {origin: 0}
    to_visit = deque([origin])

    def next_nodes(node):
        nodes = set(graph[center].orbited_by)
        if not directed:
            nodes.update(graph[center].orbits)
        return nodes
    while to_visit:
        center = to_visit.popleft() if order == 'bfs' else to_visit.popright()
        for satelite in next_nodes(center):
            if satelite in node_vals:
                continue
            if result:=process_func(node_vals, center, satelite) == 'exit':
                return
            to_visit.append(satelite)
    return node_vals


def count_orbits(graph):
    def determine_num_orbits(nodes_num_orbits, center, satelite):
        nodes_num_orbits[satelite] = nodes_num_orbits[center]+1

    nodes_orbits = traverse_graph(graph, 'COM', determine_num_orbits)
    return sum(nodes_orbits.values())


def minimum_transfers_to_santa(graph, origin='YOU', dest='SAN'):
    def determine_distance(nodes_distance, center, satelite):
        nodes_distance[satelite] = nodes_distance[center]+1
        if center == dest:
            return 'exit'
    distances = traverse_graph(graph, origin, determine_distance,
                               directed=False)
    return distances[dest] - 2


orbit_strs = map(lambda s: s.strip(), open('input.txt', 'r').readlines())
orbits = list(map(parse_orbit, orbit_strs))
graph = build_graph(orbits)

# part 1
count = count_orbits(graph)
pprint(count)

distances = minimum_transfers_to_santa(graph)
pprint(distances)
