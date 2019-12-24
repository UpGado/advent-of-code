from santavm import SantaVM
from io import StringIO
from more_itertools import chunked
import time


def arcade_output(codes):
    outio = StringIO()
    m = SantaVM(codes, output_stream=outio)
    m.run_forever()
    return outio.getvalue()


def parse_arcade_output(output):
    nums = list(map(int, output.split('\n')[:-1]))  # last element is a space
    tiles = {(x, y): tile for [x, y, tile] in chunked(nums, 3)}
    return tiles


codes = [int(num) for num in open('input.txt', 'r').read().split(',')]

# part 1
tiles = parse_arcade_output(arcade_output(codes))
count_blocks = sum([t == 2 for t in tiles.values()])
print(count_blocks)


# part 2
def display_screen(tiles, score):
    tile_shapes = {0: ' ', 1: '█', 2: '◉', 3: '__', 4: 'O'}
    x_coords, y_coords = [[c[dim] for c in tiles.keys()] for dim in range(2)]
    x_range, y_range = map(lambda cs: range(min(cs), max(cs)+1),
                           (x_coords, y_coords))
    for y in y_range:
        for x in x_range:
            tile_id = tiles.get((x, y), 0)
            print(tile_shapes[tile_id], end='')
        print('')
    print(f'Score={score}')


def get_score(coords):
    score_coord = (-1, 0)
    if score_coord in coords:
        return coords.pop(score_coord)
    else:
        return None


def get_action(tiles):
    find_tile = lambda tile_id: [coord for coord, id in tiles.items() if id ==
                                 tile_id][0]
    paddle_x, _ = find_tile(3)
    ball_x, _ = find_tile(4)
    if paddle_x > ball_x:
        return -1
    elif paddle_x < ball_x:
        return 1
    else:
        return 0


def arcade_with_screen(codes, display=True):
    coords = {}
    outio = StringIO()
    inio = StringIO()
    m = SantaVM(codes, input_stream=inio, output_stream=outio)
    score = 0
    try:
        while True:
            m.run_until(opcode='03')
            coords.update(parse_arcade_output(outio.getvalue()))
            score = get_score(coords) or score
            if display:
                display_screen(coords, score)
                time.sleep(0.01)
            outio.truncate(0)
            outio.seek(0)
            print(get_action(coords), file=inio)
            m.step()
    except StopIteration:
        return score


codes[0] = 2
score = arcade_with_screen(codes, display=False)
print(score)
