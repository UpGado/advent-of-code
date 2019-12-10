from math import floor


def fuel(mass):
    return floor(mass/3)-2


def fuel_with_fuel(mass):
    f = fuel(mass)
    return 0 if f <= 0 else f + fuel_with_fuel(f)


# use fuel instead of fuel_with_fuel for part 1
print(sum((fuel_with_fuel(int(mass)) for mass in open('puzzle_1_input', 'r'))))
