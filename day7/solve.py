from itertools import permutations
from more_itertools import pairwise
from santavm import SantaVM
from io import StringIO


def run_amplification_circuit(codes, phase_sequence):
    output = 0
    for phase in phase_sequence:
        inio = StringIO('\n'.join(map(str, [phase, output])))
        outio = StringIO()
        m = SantaVM(codes, input_stream=inio, output_stream=outio)
        m.run_forever()
        outio.seek(0)
        output = int(outio.read())
    return output


codes = [int(num) for num in open('input.txt', 'r').read().split(',')]


# part 1
possible_phase_sequences = permutations(range(0, 4+1), 5)
best_phase_sequence = max(possible_phase_sequences, key=lambda s:
                          run_amplification_circuit(codes, s))
maximum_output = run_amplification_circuit(codes, best_phase_sequence)
print(best_phase_sequence, maximum_output)


'''
- Every output stream of a machine is the input stream of the machine

    O-------O out  O-------O out  O-------O out
  .>| Amp A |----->| Amp B |----->| Amp C |--.
in| O-------O   in O-------O   in O-------O  |
  '------------------------------------------'
'''


# part 2
def run_amplification_circuit_with_feedback(codes, phase_sequence):
    n_machines = len(phase_sequence)
    streams = [StringIO() for _ in range(n_machines)]
    # simulate wrapping around list when iterating
    streams = [streams[-1], *streams]

    def new_machine(inio, outio):
        return SantaVM(codes, input_stream=inio, output_stream=outio)

    machines = [new_machine(inio, outio) for inio, outio in pairwise(streams)]

    assert machines[0].output_stream is machines[1].input_stream
    assert machines[-1].output_stream is machines[0].input_stream

    # give every machine its phase
    for machine, phase in zip(machines, phase_sequence):
        machine.run_until(opcode='03')
        inio = machine.input_stream
        print(phase, file=inio)
        machine.step()

    print(0, file=machines[0].input_stream)
    try:
        while True:
            for m, machine in enumerate(machines):
                machine.run_until(opcode='04')
                machine.step()
    except StopIteration:
        outio = machines[-1].output_stream
        outio.seek(0)
        last_output = outio.readlines()[-1]
        return int(last_output)


possible_phase_sequences = permutations(range(5, 9+1), 5)
best_phase_sequence = max(possible_phase_sequences, key=lambda s:
                          run_amplification_circuit_with_feedback(codes, s))
maximum_output = run_amplification_circuit_with_feedback(codes,
                                                         best_phase_sequence)
print(best_phase_sequence, maximum_output)
