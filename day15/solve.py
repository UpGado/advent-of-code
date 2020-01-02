from santavm import SantaVM
from collections import deque

UP, DOWN, LEFT, RIGHT = range(1, 4+1)
WALL, SPACE, OXYGEN = range(2+1)


def display_env(env, base=None):
    UNKNOWN = -1
    tile_shapes = {WALL: '█', SPACE: '.', OXYGEN: '$', UNKNOWN: '?'}
    x_coords, y_coords = [[c[dim] for c in env.keys()] for dim in range(2)]
    x_range, y_range = map(lambda cs: range(min(cs), max(cs)+1),
                           (x_coords, y_coords))
    for x in x_range:
        for y in y_range:
            tile_id = env.get((x, y), UNKNOWN)
            if (x, y) == (0, 0):
                shape = 'G'
            elif (x, y) == base:
                shape = 'B'
            else:
                shape = tile_shapes[tile_id]
            print(shape, end='')
        print('')
    print('')


def bordering_coords(coords):
    x0, y0 = coords
    return [(UP,    (x0-1, y0)),
            (LEFT,  (x0, y0-1)),
            (DOWN,  (x0+1, y0)),
            (RIGHT, (x0, y0+1))]


def reverse_action(action):
    reverse = {UP: DOWN, DOWN: UP,
               LEFT: RIGHT, RIGHT: LEFT}
    return reverse[action]


def goto_base(machine, base, directions):
    '''Returns a machine that is at the requested base'''
    # I wish I could do this recursively, but Python can't handle that'''
    for movement in enumerate_movements(base, directions):
        print(movement, file=machine.input_stream)
        machine.run_until(opcode='04', including=True)


def enumerate_movements(base, directions):
    movements = deque()
    while base != (0, 0):
        prev_base, action = directions[base]
        movements.appendleft(action)
        base = prev_base
    return movements


def look_around_base(base, env, directions):
    def extract_tile(machine):
        text = machine.output_stream.getvalue()
        num = int(text.splitlines()[-1])
        return num
    new_env = {}
    new_directions = {}
    machine = SantaVM.with_streams(codes)
    goto_base(machine, base, directions)
    for action, coord in bordering_coords(base):
        if coord in env:
            continue
        print(action, file=machine.input_stream)
        machine.run_until(opcode='04', including=True)
        tile = extract_tile(machine)
        new_env[coord] = tile
        new_directions[coord] = (base, action)
        if tile == SPACE:
            print(reverse_action(action), file=machine.input_stream)
            machine.run_until(opcode='04', including=True)
            assert(extract_tile(machine) == env[base])
    return new_env, new_directions


def discover_env(codes, verbose=True):
    '''My approach is to spawn many machines from any known location and then
    do one movement, revealing what's in an unknown location, now this location
    is known, so start from there and recurse'''
    prev_bases = []
    next_bases = [(0, 0)]
    directions = {}
    env = {(0, 0): SPACE}
    while next_bases:
        base = next_bases.pop()
        new_env, new_directions = look_around_base(base, env, directions)
        env.update(new_env)
        directions.update(new_directions)
        spaces = [coord for coord, type in new_env.items()
                  if type != WALL and coord not in prev_bases]
        next_bases.extend(spaces)
        prev_bases.append(base)
        if verbose:
            display_env(env, base=base)
    return env, directions


codes = [int(num) for num in open('input.txt', 'r').read().split(',')]
env, directions = discover_env(codes)


# part 1
oxygen_coord = [coord for coord, type in env.items() if type == OXYGEN][0]
movements = enumerate_movements(oxygen_coord, directions)
print(len(movements))


# part 2
def diffuse_oxygen(env):
    def oxygen_coords():
        return {coord: OXYGEN for coord, type in env.items() if type == OXYGEN}
    minutes = 0
    while SPACE in env.values():
        for coord in oxygen_coords().keys():
            for _, adj_coord in bordering_coords(coord):
                if env[adj_coord] != WALL:
                    env[adj_coord] = OXYGEN
        minutes += 1
    return minutes


print(diffuse_oxygen(env))
