import math


def fuel(mass):
    return math.floor(mass/3)-2


def fuel_with_fuel(mass):
    return 0 if fuel(mass) <= 0 else fuel(mass) + fuel_with_fuel(fuel(mass))


print(sum((fuel_with_fuel(int(mass)) for mass in open('puzzle_1_input', 'r'))))
