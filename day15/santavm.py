from more_itertools import seekable, padded
from functools import partial
from collections import namedtuple
from io import StringIO
from sys import stdin, stdout

Instruction = namedtuple('Instruction', 'nargs func')


class BinaryInstruction(Instruction):
    def __new__(cls, operator):
        def func(codes, source1, source2, dest):
            dest[0] = operator(source1[0], source2[0])
        return super(BinaryInstruction, cls).__new__(cls, 3, func)


class SantaVM(object):

    MEM_SIZE = 10000

    class Halt(Exception):
        pass

    def __init__(self, codes, input_stream=stdin, output_stream=stdout):
        self.codes = [[num] for num in padded(codes, fillvalue=0,
                                              n=self.MEM_SIZE)]
        self.input_stream = input_stream
        self.input_offset = 0
        self.output_stream = output_stream
        self.output_offset = 0
        self._setup_opcodes()
        self.state = self._run()
        self.relative_base = 0

    @classmethod
    def fromfile(cls, filepath, *args, **kwargs):
        codes = [int(num) for num in open(filepath, 'r').read().split(',')]
        return cls(codes, *args, **kwargs)

    @classmethod
    def with_streams(cls, codes):
        inio = StringIO()
        outio = StringIO()
        machine = cls(codes, input_stream=inio, output_stream=outio)
        return machine

    def _halt(self, codes):
        raise self.Halt

    def _input_num(self, codes, dest):
        self.input_stream.seek(self.input_offset)
        line = self.input_stream.readline()
        dest[0] = int(line)
        self.input_offset = self.input_stream.tell()

    def _output_num(self, codes, source):
        print(source[0], file=self.output_stream)

    def _change_relative_base(self, codes, source):
        self.relative_base += source[0]

    def _jump(self, codes, tested_value, dest, test=None):
        if test(tested_value[0]):
            return {'seek_to': dest[0]}

    def _setup_opcodes(self):
        self.opcodes = {'01': BinaryInstruction(lambda x, y: x+y),
                        '02': BinaryInstruction(lambda x, y: x*y),
                        '03': Instruction(1, self._input_num),
                        '04': Instruction(1, self._output_num),
                        '05': Instruction(2, partial(self._jump,
                                                     test=lambda x: x != 0)),
                        '06': Instruction(2, partial(self._jump,
                                                     test=lambda x: x == 0)),
                        '07': BinaryInstruction(lambda x, y: int(x < y)),
                        '08': BinaryInstruction(lambda x, y: int(x == y)),
                        '09': Instruction(1, self._change_relative_base),
                        '99': Instruction(0, self._halt)}

    def _get_params(self, codes, param_modes, pos, nargs):
        param_nums = codes[pos+1:pos+nargs+1]
        return [codes[num] if mode == '0'
                else [num] if mode == '1'
                else codes[self.relative_base+num]
                for (mode, [num]) in zip(param_modes, param_nums)]

    def _parse_opcode_num(self, codes, opcode_num, pos):
        opcode_str = f'{opcode_num:05d}'
        param_modes = opcode_str[:-2][::-1]
        opcode = opcode_str[-2:]
        instruction = self.opcodes[opcode]
        nargs, func = instruction
        offset = nargs+1
        params = self._get_params(codes, param_modes, pos, nargs)
        return func, params, offset, opcode

    def _run(self):
        it = seekable(enumerate(self.codes))
        for pos, [opcode_num] in it:
            func, params, offset, opcode = self._parse_opcode_num(self.codes,
                                                                  opcode_num,
                                                                  pos)
            yield {'opcode': opcode}
            try:
                result = func(self.codes, *params) or {}
                it.seek(result.get('seek_to', pos+offset))
            except self.Halt:
                return

    def run_forever(self):
        for _ in self.state:
            pass

    def run_until(self, opcode, including=False):
        for state in self.state:
            if state['opcode'] == opcode:
                if including:
                    self.step()
                return

    def step(self):
        next(self.state)
