from santavm import SantaVM
from io import StringIO
from collections import defaultdict
from math import radians, cos, sin


def add_vectors(v1, v2):
    return tuple(sum(xs) for xs in zip(v1, v2))


def angle_to_vector(angle):
    angle = radians(angle)
    return tuple(round(x) for x in (-sin(angle), cos(angle)))


def run_robot_on_map(codes_file, initial_color=0):
    inio = StringIO('0')
    outio = StringIO()
    pos = (0, 0)
    angle = 90
    terrain = defaultdict(lambda: 0)
    terrain[pos] = initial_color
    m = SantaVM.fromfile(codes_file, input_stream=inio, output_stream=outio)
    while True:
        try:
            print(terrain[pos], file=inio)
            m.run_until(opcode='04')
            m.run_until(opcode='04')
            m.step()
            outio.seek(0)
            new_color, direction = map(int, outio.readlines())
            terrain[pos] = new_color
            if direction == 0:
                angle += 90
            elif direction == 1:
                angle -= 90
            angle = angle % 360
            pos = add_vectors(pos, angle_to_vector(angle))
            outio.truncate(0)
            outio.seek(0)
        except StopIteration:
            return terrain


# part 1
terrain = run_robot_on_map('input.txt')
print(len(terrain))


# part 2
def print_terrain(terrain):
    x_coords, y_coords = map(lambda c: [coord[c] for coord in terrain.keys()],
                             (0, 1))
    x_range, y_range = tuple(map(lambda i: range(min(i), max(i)+1),
                                 (x_coords, y_coords)))
    for x in x_range:
        line = ''
        for y in y_range:
            line += '#' if terrain[x, y] == 1 else ' '
        print(line)


terrain = run_robot_on_map('input.txt', initial_color=1)
print_terrain(terrain)
