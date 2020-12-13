from io import StringIO
from itertools import combinations
from textwrap import dedent


def parse_file(file):
    return list(map(int, file))


def find_number_not_following_xmas_encryption(numbers, preamble_len=25):
    for i in range(preamble_len, len(numbers)):
        num = numbers[i]
        correct = False
        for a, b in combinations(numbers[i - preamble_len:i], 2):
            if a + b == num:
                correct = True
                break

        if not correct:
            return num


def find_encryption_weakness(list_of_numbers, number):
    for i in range(len(list_of_numbers)):
        sum = 0
        nums = set()
        j = i
        
        while sum < number:
            _num = list_of_numbers[j]
            sum += _num
            nums.add(_num)

            j += 1
        
        if sum == number:
            print(nums)
            return min(nums) + max(nums)


def test_sample_code():
    INPUT = dedent('''
        35
        20
        15
        25
        47
        40
        62
        55
        65
        95
        102
        117
        150
        182
        127
        219
        299
        277
        309
        576
    ''').strip()

    parsed = parse_file(StringIO(INPUT))

    assert find_number_not_following_xmas_encryption(parsed, 5) == 127
    assert find_encryption_weakness(parsed, 127) == 15 + 47


if __name__ == "__main__":
    with open('input.txt') as fp:
        numbers = parse_file(fp)
    
    num = find_number_not_following_xmas_encryption(numbers)
    print('Task 1: {}'.format(num))
    print('Task 2: {}'.format(find_encryption_weakness(numbers, num)))
