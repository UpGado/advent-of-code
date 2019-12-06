from more_itertools import pairwise, stagger


def has_adjacent_similar_digits(num_str):
    return any(x == y for (x, y) in pairwise(num_str))


def has_only_increasing_digits(num_str):
    return all(x <= y for (x, y) in pairwise(num_str))


def is_6_digits(num_str):
    return len(num_str) == 6


def solves_puzzle(num, predicates):
    num_str = str(num)
    return all(p(num_str) for p in predicates)


def count_solve_puzzle(num_range, predicates=None):
    return sum(solves_puzzle(i, predicates) for i in num_range)


num_range = range(256310, 732736+1)

# part 1
predicates = [is_6_digits, has_adjacent_similar_digits,
              has_only_increasing_digits]
print(count_solve_puzzle(num_range, predicates))


# part 2
def has_exactly_2_adjacent_similar_digits(num_str):
    iterator = stagger(num_str, offsets=(-2, -1, 0, 1),
                       longest=True, fillvalue='$')
    return any(v != x == y != z for (v, x, y, z) in iterator)


predicates = [is_6_digits, has_exactly_2_adjacent_similar_digits,
              has_only_increasing_digits]
print(count_solve_puzzle(num_range, predicates))
