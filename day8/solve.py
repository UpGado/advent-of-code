from skrimage import imread, imshow, binary_cmap
from more_itertools import collapse, first_true


text = open('input.txt', 'r').read().strip()
img = imread(text, (25, 6))
imshow(img)


def num_values(layer, value=0):
    return sum([pixel == value for pixel in collapse(layer)])


# part 1
layer = min(img, key=num_values)
print(num_values(layer, 1)*num_values(layer, 2))


# part 2
def flatten_img(img):
    not_transparent = lambda p: p != 2

    collapsed = [list(zip(*row)) for row in list(zip(*img))]
    flattened = [[first_true(pixels, pred=not_transparent)
                  for pixels in row] for row in collapsed]
    return [flattened]


flattened = flatten_img(img)
imshow(flattened, binary_cmap)
