from functools import partial
from itertools import islice, product
from math import prod


class Halt(Exception):
    pass


def halt(codes, pos):
    raise Halt


def _ternary_op(codes, pos, operator=None):
    source1 = codes[codes[pos+1]]
    source2 = codes[codes[pos+2]]
    codes[codes[pos+3]] = operator((source1, source2))


opcode_funcs = {1: partial(_ternary_op, operator=sum),
                2: partial(_ternary_op, operator=prod),
                99: halt}


def process(codes):
    for pos, opcode in islice(enumerate(codes), None, None, 4):
        try:
            opcode_funcs.get(opcode)(codes, pos)
        except Halt:
            return


def input(codes, input1, input2):
    codes_with_input = [codes[0], input1, input2, *codes[3:]]
    return codes_with_input


def output(codes):
    return codes[0]


original_codes = [int(num) for num in open('input.txt', 'r').read().split(',')]

# part 1
codes = input(original_codes, 12, 2)
process(codes)
print(output(codes))

# part 2
for noun, verb in product(r:= range(99+1), r):
    codes = input(original_codes, noun, verb)
    process(codes)
    if output(codes) == 19690720:
        print(100*noun + verb)
        break
