import enum
from typing import override

type TuringConfig = dict[str, str | list[str] | dict[str, dict[str, list[str]]]]
type TuringState = tuple[str, str, str]


class TuringResult(enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    INFINITE = "INFINITE"


type WholeResult = tuple[TuringResult, str] | ValueError


m = {
    "name": "1's compliment",
    "InitialState": "q0",
    "BlankSymbol": "B",
    "FinalStates": ["q2"],
    "TransitionTable": {
        "q0": {"0": ["q0", "1", "R"], "1": ["q0", "0", "R"], "B": ["q1", "B", "L"]},
        "q1": {"0": ["q1", "0", "L"], "1": ["q1", "1", "L"], "B": ["q2", "B", "R"]},
        "q2": {"0": ["", "", ""], "1": ["", "", ""], "B": ["", "", ""]},
    },
}


class TuringMachine:
    def __init__(self, config: TuringConfig) -> None:
        self.config = config
        currentState = config["InitialState"]
        if type(currentState) == str:
            self.currentState: str = currentState
        else:
            raise TypeError("Current State must be a string")
        self.pointer: int
        self.tape: list[str]

    @override
    def __repr__(self) -> str:
        return f"""## currentState  {self.currentState} ## pointer {self.pointer}"""

    def setTape(self, maybeREL: str) -> None:
        Blank = self.config["BlankSymbol"]
        if type(Blank) != str:
            raise TypeError("Tape must be a string")
        self.pointer = 1
        self.tape = list(Blank + maybeREL + Blank)

    def run(self) -> WholeResult:

        while type(self.currentState) == str:
            NextState: TuringState = self.config["TransitionTable"][self.currentState][
                self.tape[self.pointer]
            ]

            [self.currentState, write, direction] = NextState
            # print(self.currentSate in self.config["FinalStates"])
            if self.currentState in self.config["FinalStates"]:
                return TuringResult.ACCEPTED, "".join(self.tape)
            self.tape[self.pointer] = write

            if direction == "R":
                self.pointer += 1
            elif direction == "L":
                self.pointer -= 1
            else:
                return ValueError(f"Invalid Direction: {self.__repr__()}")
        return ValueError("Infinite Loop")
