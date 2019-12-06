from itertools import accumulate, repeat
from functools import reduce, partial

unit_vectors = {'U': (1, 0), 'D': (-1, 0),
                'R': (0, 1), 'L': (0, -1)}
CENTRAL_PORT = (0, 0)


def mult_vector(vector, scalar):
    return tuple(x*scalar for x in vector)


def add_vector(vector1, vector2):
    return tuple(x+y for (x, y) in zip(vector1, vector2))


def parse_vector_str(vector_list, vector_str):
    start_vector = vector_list[-1]
    direction = vector_str[0]
    magnitude = int(vector_str[1:])
    unit_vector = unit_vectors[direction]
    new_vectors = list(accumulate(repeat(unit_vector, magnitude), add_vector,
                                  initial=start_vector))[1:]
    return vector_list + new_vectors


def read_coords(line):
    return list(reduce(parse_vector_str, line.split(','), [CENTRAL_PORT]))


def get_intersections(coords):
    return set.intersection(*map(set, wires_coords)) - {CENTRAL_PORT}


lines = open('input.txt', 'r').readlines()
wires_coords = list(map(read_coords, lines))
intersections = get_intersections(wires_coords)


# part 1
def manhattan_distance(vector):
    return sum(abs(x-x0) for (x, x0) in zip(vector, CENTRAL_PORT))


closest_intersection = min(intersections, key=manhattan_distance)
print(manhattan_distance(closest_intersection))


# part 2
def combined_num_steps(coord, wires_coords=None):
    return sum((coords.index(coord) for coords in wires_coords))


_combined_num_steps = partial(combined_num_steps, wires_coords=wires_coords)
fastest_intersection = min(intersections, key=_combined_num_steps)
print(_combined_num_steps(fastest_intersection))
