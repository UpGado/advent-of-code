from itertools import repeat, cycle
from numpy import lcm


def skip_one(iterator):
    next(iterator)
    yield from iterator


def ones(num):
    return int(str(num)[-1])


def fft(nums, n_phases=1, base_seq=[0, 1, 0, -1], rep=1):
    if n_phases == 0:
        return nums
    else:
        # RECTANGULAR CODE > PEP 8
        return fft([ones(sum(num*coeff for  num,  coeff  in
                   zip(nums, skip_one(cycle( (b  for  b  in
                   base_seq for _ in range(r)))))))     for
                   r in range(1, len(nums)+1)],    n_phases
                   =n_phases-1, base_seq=base_seq, rep=rep)


def list_to_str(nums):
    return ''.join(str(x) for x in nums)


nums = [int(n) for n in open('testinput.txt').read().strip()]
# part 1
print(list_to_str(fft(nums, 100)[:8]))


# part 2

'''
nums_rep = nums*10000
num_skip = int(list_to_str(nums)[:7])
print(f'{num_skip=}')
print(list_to_str(fft(nums_rep, 100)[num_skip:num_skip+8+1]))
'''
