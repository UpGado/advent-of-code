from santavm import SantaVM

SCAFFOLD = '#'


def parse_camera(machine):
    output = machine.output_stream.getvalue()
    img = {}
    row = 0
    col = 0
    for out in output.split('\n'):
        if out != '':
            char = chr(int(out))
            if char == '\n':
                row += 1
                col = 0
            else:
                img[row, col] = char
                col += 1
    return img


def determine_ranges(coords):
    x_coords, y_coords = [[c[dim] for c in coords] for dim in range(2)]
    x_range, y_range = map(lambda cs: range(min(cs), max(cs)+1),
                           (x_coords, y_coords))
    return x_range, y_range


def imshow(img, base=None):
    x_range, y_range = determine_ranges(img.keys())
    for x in x_range:
        for y in y_range:
            shape = img[(x, y)]
            print(shape, end='')
        print('')
    print('')


def find_intersections(img):
    scaffold_coords = {coord for coord, type in img.items() if type == SCAFFOLD}
    intersections = set()
    for coord in scaffold_coords:
        x, y = coord
        neighbouring_coords = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        if all(map(lambda c: c in scaffold_coords, neighbouring_coords)):
            intersections.add(coord)
    return intersections


def alignment_params(coords):
    return [x*y for x, y in coords]


codes = [int(num) for num in open('input.txt', 'r').read().split(',')]
machine = SantaVM.with_streams(codes)
machine.run_forever()
img = parse_camera(machine)
imshow(img)
intersections = find_intersections(img)

# part 1
print(sum(alignment_params(intersections)))


# part 2
codes[0] = 2
