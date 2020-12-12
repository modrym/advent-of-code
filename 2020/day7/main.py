from collections import defaultdict, deque
from io import StringIO
from textwrap import dedent
from typing import TextIO


def parse(fp: TextIO):
    dct = defaultdict(dict)

    for line in fp:
        main_color, rest = line[:-1].split(' bags contain ')
        colors = rest.split(', ')
        
        for color in colors:
            num, color = color.split(None, 1)
            color = ' '.join(color.split()[:2])

            if num == 'no':
                continue

            dct[main_color][color] = int(num)

    return dict(dct)


def count_bags_containing_color(dct, name):
    reverse_dct = defaultdict(set)

    for main_color, d in dct.items():
        for color in d:
            reverse_dct[color].add(main_color)
    
    colors = set()
    remaining = {name}

    while remaining:
        try:
            item = remaining.pop()
        except KeyError:
            break

        colors.add(item)

        for c in reverse_dct.get(item, {}):
            if c not in colors:
                remaining.add(c)

    return len(colors) - 1


def count_bags_inside(dct, name):
    count = 0
    stack = deque()
    stack.append((name, 1))
    
    while stack:
        name, mult = stack.pop()

        if name not in dct:
            continue

        for subcolor, c in dct[name].items():
            count += c * mult
            stack.append((subcolor, c * mult))
    
    return count


def test_count_bags_containing_shiny_gold():
    TEST_STRING = dedent('''
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
        dotted black bags contain no other bags.
    ''').strip()

    assert count_bags_containing_color(parse(StringIO(TEST_STRING)), 'shiny gold') == 4


def test_count_bags_inside_1():
    TEST_STRING = dedent('''
        light red bags contain 1 bright white bag, 2 muted yellow bags.
        dark orange bags contain 3 bright white bags, 4 muted yellow bags.
        bright white bags contain 1 shiny gold bag.
        muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
        shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
        dark olive bags contain 3 faded blue bags, 4 dotted black bags.
        vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
        faded blue bags contain no other bags.
        dotted black bags contain no other bags.
    ''').strip()

    assert count_bags_inside(parse(StringIO(TEST_STRING)), 'shiny gold') == 32


def test_count_bags_inside_2():
    TEST_STRING = dedent('''
        shiny gold bags contain 2 dark red bags.
        dark red bags contain 2 dark orange bags.
        dark orange bags contain 2 dark yellow bags.
        dark yellow bags contain 2 dark green bags.
        dark green bags contain 2 dark blue bags.
        dark blue bags contain 2 dark violet bags.
        dark violet bags contain no other bags.
    ''').strip()

    assert count_bags_inside(parse(StringIO(TEST_STRING)), 'shiny gold') == 126


if __name__ == "__main__":
    with open('input.txt') as fp:
        dct = parse(fp)

    print('Task 1: {}'.format(count_bags_containing_color(dct, 'shiny gold')))
    print('Task 2: {}'.format(count_bags_inside(dct, 'shiny gold')))
