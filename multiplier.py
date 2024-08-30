import unittest

from main import TuringMachine

config = {
    "name": "multiplier",
    "InitialState": "q0",
    "BlankSymbol": "*",
    "FinalStates": ["H"],
    "TransitionTable": {
        "0": {"a": "1 * R", "*": "H * S"},
        "1": {"*": "q2 * L"},
        "2": {"0": "q3 a R", "1": "q5 b R", "*": "H * S"},
        "3": {"0": "q3 0 R", "1": "q3 1 R", "*": "q4 * R"},
        "4": {"0": "q4 0 R", "1": "q4 1 R", "*": "q7 1 L"},
        "5": {"0": "q5 0 R", "1": "q5 1 R", "*": "q6 * R"},
        "6": {"0": "q6 0 R", "1": "q6 1 R", "*": "q7 1 L"},
        "7": {
            "0": "q7 0 L",
            "1": "q7 1 L",
            "*": "q7 * L",
            "a": "q2 0 L",
            "b": "q2 1 L",
        },
        "H": {"0": [], "1": [], "*": []},
    },
}


class CopyStringTest(unittest.TestCase):

    def testCopyString(self):
        tm = TuringMachine(config)
        tm.setTape("000111")
        try:
            print(tm.run(withLogs=True))
        except ValueError:
            self.fail
        self.assertEqual(tm.tape, "*000111*000111*")
