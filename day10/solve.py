import numpy as np


def find_asteroids(terrain):
    return [(int(x), int(y)) for x, y in zip(*np.nonzero(terrain == '#'))]


def shine_laser_clockwise(terrain, base):
    height, width = terrain.shape
    xv, yv = np.meshgrid(range(height), range(width), indexing='ij')
    x0, y0 = base
    distances = np.sqrt((xv-x0)**2+(yv-y0)**2)
    angles = np.arctan2(-(xv-x0), -(yv-y0))-np.pi/2
    angles = np.mod(angles, 2*np.pi)

    for angle in np.unique(angles.flatten()):
        ray_mask = angles == angle
        ray_coords = []
        for distance in np.sort(distances[ray_mask].flatten()):
            x, y = np.nonzero((ray_mask) & (distances == distance))
            if (x, y) != base:
                ray_coords.append((x, y))
        yield ray_coords


terrain = [list(line.strip()) for line in open('input.txt').readlines()]
terrain = np.array(terrain)


# part 1
def count_line_of_sight(terrain, base):
    in_line_of_sight = 0
    for ray_coords in shine_laser_clockwise(terrain, base):
        in_line_of_sight += any(terrain[x, y] == '#' for x, y in ray_coords)
    return in_line_of_sight


asteroids = find_asteroids(terrain)
best_astroid = max(asteroids, key=lambda a: count_line_of_sight(terrain, a))
print(count_line_of_sight(terrain, best_astroid))


# part 2
def shoot_laser(terrain, base, max=None):
    shot_asteroids = []
    terrain = np.copy(terrain)
    terrain[base] == 'B'
    while find_asteroids(terrain):
        for ray_coords in shine_laser_clockwise(terrain, base):
            asteroids_in_ray = [coord for coord in ray_coords if
                                terrain[coord] == '#']
            if asteroids_in_ray:
                closest_asteroid = asteroids_in_ray[0]
                terrain[closest_asteroid] = '.'
                print(f'destroyed {closest_asteroid}')
                shot_asteroids.append(closest_asteroid)
        if max and len(shot_asteroids) >= max:
            return shot_asteroids
    return shot_asteroids


destroyed = shoot_laser(terrain, best_astroid, 200)
print(destroyed[200-1])
