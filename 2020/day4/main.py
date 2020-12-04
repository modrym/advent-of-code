import re
from textwrap import dedent


def parse(string):
    results = []

    for i, entry in enumerate(string.split('\n\n')):
        spli = [i.split(':') for i in entry.split()]
        dct = {n:v for n, v in spli}

        if len(spli) != len(dct):
            # Some fields are repeated
            continue
    
        results.append(dct)

    return results


def get_records_with_valid_field_names(records):
    results = []
    VALID_FIELDS = {
        'byr',
        'iyr',
        'eyr',
        'hgt',
        'hcl',
        'ecl',
        'pid'
    }

    OPTIONAL_FIELDS = {'cid'}

    for record in records:
        if record.keys() - OPTIONAL_FIELDS == VALID_FIELDS:
            results.append(record)

    return results


def get_records_with_valid_values(records):
    results = []
    
    hcl_pat = re.compile(r'#[0-9a-f]{6}')
    ecl = 'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'

    for r in records:
        try:
            int(r['pid'])
            
            if len(r['pid']) != 9:
                continue
            
            if not 1920 <= int(r['byr']) <= 2002:
                continue

            if not 2010 <= int(r['iyr']) <= 2020:
                continue

            if not 2020 <= int(r['eyr']) <= 2030:
                continue

            if not r['hgt'].endswith(('cm', 'in')):
                continue

            hgt = int(r['hgt'][:-2])
            unit = r['hgt'][-2:]
            
            if not (unit == 'cm' and 150 <= hgt <= 193 \
                    or unit == 'in' and 59 <= hgt <= 76):
                continue

            if not hcl_pat.match(r['hcl']):
                continue

            if r['ecl'] not in ecl:
                continue
        except ValueError:
            continue

        results.append(r)

    return results


def test_part1():
    TEST_DATA = dedent('''
        ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
        byr:1937 iyr:2017 cid:147 hgt:183cm

        iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
        hcl:#cfa07d byr:1929

        hcl:#ae17e1 iyr:2013
        eyr:2024
        ecl:brn pid:760753108 byr:1931
        hgt:179cm

        hcl:#cfa07d eyr:2025 pid:166559648
        iyr:2011 ecl:brn hgt:59in
    ''').strip()

    assert len(get_records_with_valid_field_names(parse(TEST_DATA))) == 2


def test_part2_invalid():
    TEST_DATA = dedent('''
        eyr:1972 cid:100
        hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

        iyr:2019
        hcl:#602927 eyr:1967 hgt:170cm
        ecl:grn pid:012533040 byr:1946

        hcl:dab227 iyr:2012
        ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

        hgt:59cm ecl:zzz
        eyr:2038 hcl:74454a iyr:2023
        pid:3556412378 byr:2007
    ''').strip()
    
    assert not get_records_with_valid_values(parse(TEST_DATA))


def test_part2_valid():
    TEST_DATA = dedent('''
        pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
        hcl:#623a2f

        eyr:2029 ecl:blu cid:129 byr:1989
        iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

        hcl:#888785
        hgt:164cm byr:2001 iyr:2015 cid:88
        pid:545766238 ecl:hzl
        eyr:2022

        iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
    ''').strip()
    
    assert len(get_records_with_valid_values(parse(TEST_DATA))) == 4


if __name__ == '__main__':
    with open('input.txt') as fp:
        input_data = fp.read()
        
    records = get_records_with_valid_field_names(parse(input_data))
    
    print('Task 1: {}'.format(len(records)))
    print('Task 2: {}'.format(len(get_records_with_valid_values(records))))
