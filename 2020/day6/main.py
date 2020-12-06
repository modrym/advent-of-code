import operator
from functools import reduce
from textwrap import dedent


def sum_of_counts_anyone(string):
    return sum(
        len(
            set(''.join(group.split()))
        ) for group in string.split('\n\n')
    )


def sum_of_counts_everyone(string):
    return sum(
        len(
            reduce(
                operator.and_,
                (set(i) for i in group.split())
            )
        ) for group in string.split('\n\n')
    )


TEST_STRING = dedent('''
    abc

    a
    b
    c

    ab
    ac

    a
    a
    a
    a

    b
''').strip()


def test_sum_of_counts_anyone(): 
    assert sum_of_counts_anyone(TEST_STRING) == 11


def test_sum_of_counts_everyone():
    assert sum_of_counts_everyone(TEST_STRING) == 6


if __name__ == "__main__":
    with open('input.txt') as fp:
        input = fp.read()
    
    print('Task 1: {}'.format(sum_of_counts_anyone(input)))
    print('Task 2: {}'.format(sum_of_counts_everyone(input)))
