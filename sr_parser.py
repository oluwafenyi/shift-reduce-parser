from collections import deque, defaultdict

# Grammar rules
# Equation := Variable - expression
# Variable := y
# expression := term | expression + term
# term := factor | term/ factor
# factor := constant | n | x | nx | nx power | factor . n . x. power
# constant := integer | integer!
# n := n | (n-integer)
# power := ^integer
# integer := digit | digit. integer
# digit := 0| 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |

class SRParser:
    rightmost_literal_map: set
    derivation_to_non_terminal_map: defaultdict
    start_symbol: str

    def __init__(self):
        self.rightmost_literal_map = set()
        self.derivation_to_non_terminal_map = defaultdict(lambda: None)

    def set_start_symbol(self, symbol):
        self.start_symbol = symbol

    def load_terminals(self, list):
        self.terminals = set(list)

    def load_grammar_rule(self, non_terminal, production_rule):
        self.derivation_to_non_terminal_map[production_rule] = non_terminal
        rightmost_literal = production_rule.split()[-1]
        self.rightmost_literal_map.add(rightmost_literal)
        self.rightmost_literal_map.add(rightmost_literal[-1])

    def _attempt_reduce(self, stack: deque, character):
        if (character == "$"):
            literal_list = []

            while len(stack) > 0:
                literal_list = [stack.pop(), *literal_list]

            literals = "".join(literal_list)[:-1]

            if (literals in self.derivation_to_non_terminal_map):
                non_terminal = self.derivation_to_non_terminal_map[literals]

                stack.append(non_terminal)
                print(f"\nReducing by {non_terminal} -> {literals}")
                print(f"Stack = {stack}")
                return

        elif (character in self.rightmost_literal_map):
            literal_list = []

            while len(stack) > 0:
                literal_list = [stack.pop(), *literal_list]

            if (len(literal_list) == 1):
                literals = literal_list[0]
                non_terminal = self.derivation_to_non_terminal_map[literals]
                stack.append(non_terminal)
                print(f"\nReducing by {non_terminal} -> {literals}")
                print(f"Stack = {stack}")
                return

            for i in range(len(literal_list)):
                literals = "".join(literal_list[i:])

                if (literals in self.derivation_to_non_terminal_map):
                    non_terminal = self.derivation_to_non_terminal_map[literals]

                    for l in literal_list[:i]:
                        stack.append(l)

                    stack.append(non_terminal)
                    print(f"\nReducing by {non_terminal} -> {literals}")
                    print(f"Stack = {stack}")
                    return self._attempt_reduce(stack, non_terminal)

            for element in literal_list:
                stack.append(element)


    def parse_input(self, input_string):
        stack = deque()

        print(f"Stack = {stack}")

        for i, character in enumerate(input_string):
            if (character == " "):
                continue

            stack.append(character)
            print(f"\nShift: {character}")
            print(f"Stack = {stack}")

            if i + 1 < len(input_string) and input_string[i+1] == ".":
                continue

            self._attempt_reduce(stack, character)

        last_token = stack.pop()
        if last_token == self.start_symbol:
            print("\nParsed: VALID STRING")
            return True

        print("\nCould Not Parse: STRING INVALID")
        return False


if __name__ == "__main__":
    rules = [
        ("<equation>", "<variable>=<expression>"),
        ("<equation>", "<variable>=<expression>+<expression>"),
        ("<variable>", "y"),
        ("<expression>", "<term>"),
        ("<expression>", "<expression>+<term>"),
        ("<expression>", "<expression>/<expression>"),
        ("<expression>", "(<expression>-<expression>)"),
        ("<expression>", "(<expression>-<expression>).x"),
        ("<expression>", "<expression>!"),
        ("<expression>", "<expression>+(<expression>)"),
        ("<expression>", "(n.<expression><power>/<expression>)"),
        ("<term>", "<expression>/(<expression>)"),
        ("<expression>", "(n.<expression><power>)"),
        ("<term>", "<factor>"),
        ("<term>", "<term>/<factor>"),
        ("<factor>", "<constant>"),
        ("<factor>", "n"),
        ("<factor>", "x"),
        ("<factor>", "n.x"),
        ("<factor>", "n.x<power>"),
        ("<factor>", "<factor>n.x<power>"),
        ("<constant>", "<integer>"),
        ("<constant>", "<integer>!"),
        ("n", "(n-<integer>)"),
        ("<power>", "^<integer>"),
        ("<integer>", "<digit>"),
        ("<integer>", "<digit><integer>"),
        ("<digit>", "0"),
        ("<digit>", "1"),
        ("<digit>", "2"),
        ("<digit>", "3"),
        ("<digit>", "4"),
        ("<digit>", "5"),
        ("<digit>", "6"),
        ("<digit>", "7"),
        ("<digit>", "8"),
        ("<digit>", "9"),
    ]

    shift_reduce_parser = SRParser()

    shift_reduce_parser.set_start_symbol("<equation>")

    for rule in rules:
        non_terminal, production_rule = rule
        shift_reduce_parser.load_grammar_rule(non_terminal, production_rule)


    input_string = "y = 1 + (n.x) / (1!) + (n.(n-1).x^2) / (2!) + (n.(n-2).x^3 / 3!) + (n.(n-3).x^4) / (4!)$"

    shift_reduce_parser.parse_input(input_string)
