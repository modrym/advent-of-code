from textwrap import dedent


class CodeParser:
    def __init__(self, program):
        self._program = [line.split(None, 2) for line in program.splitlines()]
        self._line = 0
        self._len = len(self._program)
        self.accumulator = 0
        self.terminated = False
    
    def clear(self):
        self.accumulator = 0
        self._line = 0
        self.terminated = False

    def run_without_repeats(self):
        line_set = set()

        while self._line < self._len:
            if self._line in line_set:
                return

            line_set.add(self._line)
            self.run_command()
        
        self.terminated = True

    def run_command(self):
        cmd, arg = self._program[self._line]
        self._line += 1
        return getattr(self, cmd)(int(arg))

    @staticmethod
    def nop(arg):
        pass

    def jmp(self, arg):
        self._line += arg - 1
    
    def acc(self, arg):
        self.accumulator += arg

    def swap_jmp_nop(self, num):
        lst = self._program[num]

        if lst[0] == 'jmp':
            lst[0] = 'nop'
        elif lst[0] == 'nop':
            lst[0] = 'jmp'
        else:
            return False

        return True


def fix_instruction_and_run(parser):
    for i in range(parser._len):
        if not parser.swap_jmp_nop(i):
            continue

        parser.clear()
        parser.run_without_repeats()
        
        if not parser.terminated:
            parser.swap_jmp_nop(i)
            continue

        return i


def test_sample_program():
    TEST_STRING = dedent('''
        nop +0
        acc +1
        jmp +4
        acc +3
        jmp -3
        acc -99
        acc +1
        jmp -4
        acc +6
    ''').strip()

    parser = CodeParser(TEST_STRING)
    parser.run_without_repeats()

    assert parser.accumulator == 5

    fix_instruction_and_run(parser)
    assert parser.accumulator == 8


if __name__ == "__main__":
    with open('input.txt') as fp:
        program = fp.read()
    
    parser = CodeParser(program)
    parser.run_without_repeats()
    print('Task 1: {}'.format(parser.accumulator))

    line = fix_instruction_and_run(parser)
    print('Task 2: broken line {}, accumulator: {}'.format(line, parser.accumulator))
