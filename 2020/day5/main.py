def decode_seat_id(string):
    if len(string) != 10:
        raise ValueError('Incorrect boarding pass')

    # Get first 7 characters and revert them
    # B - binary 1, F - binary 0
    row = sum(2 ** i for i, c in enumerate(string[:7][::-1]) if c == 'B')

    # Get last 3 characters and revert them
    # R - binary 1, L - binary 0
    col = sum(2 ** i for i, c in enumerate(string[7:][::-1]) if c == 'R')

    return row * 8 + col


def find_missing_seat(ids):
    ids = sorted(ids)
    previous = ids[0]
    
    for i in range(1, len(ids)):
        num = ids[i]
        if num != previous + 1:
            return previous + 1

        previous = num


def test_decode_examples():
    assert decode_seat_id('BFFFBBFRRR') == 567
    assert decode_seat_id('FFFBBBFRRR') == 119
    assert decode_seat_id('BBFFBBFRLL') == 820
    

def test_missing_seats():
    assert find_missing_seat([1, 2, 3, 4, 6]) == 5
    assert find_missing_seat([6, 4, 3, 2, 1]) == 5
    assert find_missing_seat([7, 5, 9, 3, 6, 8, 4, 2, 0]) == 1


if __name__ == '__main__':
    with open('input.txt') as fp:
        content = fp.read()

    seat_ids = [decode_seat_id(s) for s in content.split()]
    print('Task 1: {}'.format(max(seat_ids)))
    print('Task 2: {}'.format(find_missing_seat(seat_ids)))
