from more_itertools import chunked


def imread(text, size):
    cols, rows = size
    pixels_per_layer = cols*rows

    img = [[[int(element) for element in row]
           for row in chunked(layer, cols)]
           for layer in chunked(text, pixels_per_layer)]
    return img


gray_cmap = {0: lambda t: f'\u001b[38;5;240m{t}\u001b[0m',
             1: lambda t: f'\u001b[38;5;241m{t}\u001b[0m',
             2: lambda t: f'\u001b[38;5;242m{t}\u001b[0m',
             3: lambda t: f'\u001b[38;5;243m{t}\u001b[0m',
             4: lambda t: f'\u001b[38;5;245m{t}\u001b[0m',
             5: lambda t: f'\u001b[38;5;246m{t}\u001b[0m',
             6: lambda t: f'\u001b[38;5;247m{t}\u001b[0m',
             7: lambda t: f'\u001b[38;5;248m{t}\u001b[0m',
             8: lambda t: f'\u001b[38;5;249m{t}\u001b[0m',
             9: lambda t: f'\u001b[38;5;250m{t}\u001b[0m',
             }


binary_cmap = {0: lambda t: f'\u001b[38;5;240m{t}\u001b[0m',
               1: lambda t: f'\u001b[38;5;250m{t}\u001b[0m'}


def apply_cmap(pixel, cmap):
    return cmap[pixel](pixel)


def imshow(img, cmap=gray_cmap):
    for i, layer in enumerate(img):
        print('layer', i)
        for row in layer:
            for pixel in row:
                print(apply_cmap(pixel, cmap), end='')
            print('')
