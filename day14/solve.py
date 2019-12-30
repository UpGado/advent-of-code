from more_itertools import pairwise
from pprint import pprint
from collections import defaultdict
from math import ceil


def read_reactions(filename):
    lines = open(filename).readlines()
    reactions = {}
    for line in lines:
        ins, out = [[(int(num), name)
                     for m in side.strip().split(',')
                     for num, name in pairwise(m.strip().split(' '))]
                    for side in line.split('=>')]
        out_num, out_name = out[0]  # there is only one output molecule.
        ins_dict = {name: num for (num, name) in ins}
        reactions[out_name] = (out_num, ins_dict)
    return reactions


def rank_graph(reactions, ranks=defaultdict(lambda: 0), root='FUEL'):
    '''The idea here is to assign each molecule a number that shows how complex
    it is, with FUEL being the most complex (highest number), and ORE being the
    simplest (lowest number'''
    if root in reactions:
        components = reactions[root][1].keys()
        for component in components:
            new_rank = ranks[root] - 1
            if ranks[component] > new_rank:
                ranks[component] = new_rank
            rank_graph(reactions, ranks, root=component)
    return ranks


reactions = read_reactions('input.txt')
ranks = rank_graph(reactions)


# part 1
def simplify_bag(bag, reactions, ranks):
    _bag = defaultdict(lambda: 0)
    _bag.update(bag)
    bag = _bag
    while any(item in reactions for item in bag):
        item, quantity = max(bag.items(), key=lambda i: ranks[i[0]])
        min_quantity, components = reactions[item]
        n_reactions = ceil(-(-quantity//min_quantity))
        for component, amount in components.items():
            bag[component] += amount*n_reactions
        bag[item] -= quantity
        if bag[item] == 0:
            bag.pop(item)
    return dict(bag)


pprint(simplify_bag({'FUEL': 1}, reactions, ranks))


# part 2
def maximum_fuel(num_ore, reactions, ranks):
    '''Let's use binary search cuz why not'''
    max_guess = num_ore
    min_guess = 1
    while True:
        guess = (max_guess+min_guess)//2
        bag = simplify_bag({'FUEL': guess}, reactions, ranks)
        print(guess, '=>', bag['ORE'])
        if bag['ORE'] == num_ore or (max_guess - min_guess) == 1:
            return guess  # perfect match
        elif bag['ORE'] > num_ore:
            max_guess = guess
        elif bag['ORE'] < num_ore:
            min_guess = guess


print(maximum_fuel(int(1E12), reactions, ranks))
