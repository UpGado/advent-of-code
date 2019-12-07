from more_itertools import seekable
from functools import partial
from collections import namedtuple


Instruction = namedtuple('Instruction', ['nargs', 'func'])


def TernaryInstruction(operator):
    return Instruction(3, partial(_ternary_op, operator=operator))


class Halt(Exception):
    pass


def halt(codes):
    raise Halt


def _ternary_op(codes, source1, source2, dest, operator=None):
    dest[0] = operator(source1[0], source2[0])


def input_num(codes, dest):
    dest[0] = int(input('Input: '))


def output_num(codes, source):
    print('Output:', source[0])


def jump(codes, tested_value, dest, test=None):
    if test(tested_value[0]):
        return {'seek_to': dest[0]}


opcodes = {'01': TernaryInstruction(lambda x, y: x+y),
           '02': TernaryInstruction(lambda x, y: x*y),
           '03': Instruction(1, input_num),
           '04': Instruction(1, output_num),
           '05': Instruction(2, partial(jump, test=lambda x: x != 0)),
           '06': Instruction(2, partial(jump, test=lambda x: x == 0)),
           '07': TernaryInstruction(lambda x, y: int(x < y)),
           '08': TernaryInstruction(lambda x, y: int(x == y)),
           '99': Instruction(0, halt)}


def get_params(codes, param_modes, pos, nargs):
    param_nums = codes[pos+1:pos+nargs+1]
    return [codes[num] if mode == '0' else [num]
            for (mode, [num]) in zip(param_modes, param_nums)]


def parse_opcode_num(codes, opcode_num, pos):
    opcode_str = f'{opcode_num:05d}'
    param_modes = opcode_str[:-2][::-1]
    opcode = opcode_str[-2:]
    instruction = opcodes[opcode]
    nargs, func = instruction
    offset = nargs+1
    params = get_params(codes, param_modes, pos, nargs)
    return func, params, offset


def process(codes):
    it = seekable(enumerate(codes))
    for pos, [opcode_num] in it:
        func, params, offset = parse_opcode_num(codes, opcode_num, pos)
        try:
            result = func(codes, *params) or {}
            it.seek(result.get('seek_to', pos+offset))
        except Halt:
            return


while True:
    codes = [int(num) for num in open('input.txt', 'r').read().split(',')]
    codes = [[num] for num in codes]
    process(codes)
