import random
import unittest

import main

ones_compliment_config = {
    "name": "1's compliment",
    "InitialState": "q0",
    "BlankSymbol": "B",
    "FinalStates": ["q2"],
    "TransitionTable": {
        "q0": {"0": "q0 1 R", "1": "q0 0 R", "B": "q1 B L"},
        "q1": {"0": "q1 0 L", "1": "q1 1 L", "B": "q2 B R"},
        "q2": {"0": [], "1": [], "B": []},
    },
}


def genrateRandomPairs(many: int, length: int = 10) -> dict[str, str]:
    bank: dict[str, str] = {}
    for _ in range(many):
        tape = "".join(random.choices(["0", "1"], k=length))
        bank[tape] = "B" + "".join(["1" if x == "0" else "0" for x in tape]) + "B"
    return bank


class TestTuringMachine(unittest.TestCase):
    def test_setTape(self):
        t = main.TuringMachine(ones_compliment_config)
        t.setTape("1")
        self.assertEqual(t.tape, ["B", "1", "B"])
        del t

    # def test_get_from_user(self):
    #     t = main.TuringMachine(ones_compliment_config)
    #     tape = input("Enter a tape: ")
    #     t.setTape(tape)
    #     print(t.tape)
    #     comp = "B" + "".join(["1" if x == "0" else "0" for x in tape]) + "B"
    #     self.assertEqual(t.run(), (main.TuringResult.ACCEPTED, comp))
    #     print(t.tape)
    #     del t

    def test_run(self):
        t = main.TuringMachine(ones_compliment_config)
        t.setTape("101101100")
        self.assertEqual(t.run(), (main.TuringResult.ACCEPTED, "B010010011B"))
        del t

    def test_stressed(self):
        bank = genrateRandomPairs(1, 10)
        # count = 1
        for k, v in bank.items():
            t = main.TuringMachine(ones_compliment_config)
            t.setTape(k)
            # print(f"Testing {count} : \n {k} \n{v}")
            # count += 1
            self.assertEqual(t.run(), (main.TuringResult.ACCEPTED, v))
            # print(f"\n[----------\npassed \n {k}\n{v}\n----------]")
            del t
