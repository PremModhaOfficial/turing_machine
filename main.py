import enum
from typing import override

type TuringConfig = dict[str, str | list[str] | dict[str, dict[str, list[str]]]]
type TuringState = tuple[str, str, str]


class TuringResult(enum.Enum):
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"
    INFINITE = "INFINITE"

    @override
    def __str__(self) -> str:
        return self.value


type WholeResult = tuple[TuringResult, str] | ValueError


m = {
    "name": "1's compliment",
    "InitialState": "q0",
    "BlankSymbol": "B",
    "FinalStates": ["q2"],
    "TransitionTable": {
        "q0": {"0": ["q0 1 R"], "1": ["q0 0 R"], "B": ["q1 B L"]},
        "q1": {"0": ["q1 0 L"], "1": ["q1 1 L"], "B": ["q2 B R"]},
        "q2": {"0": [], "1": [], "B": []},
    },
}


class TuringMachine:
    def __init__(self, config: TuringConfig = m, withLogs=False) -> None:
        self.config = config
        currentState = config["InitialState"]
        if isinstance(currentState, str):
            self.currentState: str = currentState
        else:
            raise TypeError("Current State must be a string")
        self.pointer: int = 1
        self.tape: list[str]
        self.verbose: bool = False
        self.verboseStates = []
        self.blank: str = config["BlankSymbol"]
        self.transitionTable = config["TransitionTable"]
        self.withLogs = withLogs

    @override
    def __repr__(self) -> str:
        return f"""## currentState  {self.currentState} ## pointer {self.pointer}"""

    def extract_from_table(self):
        if self.withLogs:
            print("extracting variabels")
        if not self.transitionTable:
            return
        states = set()
        vars = set()
        for state, all_moves in self.transitionTable:
            states.add(state)
            print(all_moves)
            for nexState, move in all_moves:
                if not move or not nexState:
                    continue
                vars.add(move)
        self.vars = vars
        self.states = states

    def ttMaker(self):

        trant = str.maketrans(" ", ",")
        vars = eval("[ " + input("states saperate by ` `").translate(trant) + " ]")
        print(vars)

    def setTape(self, maybeREL: str) -> None:
        Blank = self.config["BlankSymbol"]
        if not isinstance(Blank, str):
            raise TypeError("Tape must be a string")
        self.pointer = 1
        self.tape = list(Blank + maybeREL + Blank)

    def increasePointer(self) -> None:
        self.pointer += 1
        if self.pointer >= len(self.tape):
            self.tape.append(self.blank)

    def decreasePointer(self) -> None:
        self.pointer -= 1
        if self.pointer < 0:
            self.tape.insert(0, self.blank)
            self.pointer = 0

    def compile_transition(self) -> None:
        log = str(f"{self.pointer:>4}: |- ({self.currentState}, {"".join(self.tape)})")
        # log = str(f"{self}, {"".join(self.tape)}")
        self.verboseStates.append(log)
        if self.withLogs:
            print(log)

    def trim_tape(self) -> str:
        trans = str.maketrans(self.blank, " ")
        return "".join(self.tape).translate(trans).strip()

    def printTransitions(self) -> None:
        for i in self.verboseStates:
            print(i)

    def run(self, withLogs=False) -> WholeResult:
        self.withLogs = withLogs
        if withLogs:
            print("pre while")
        while isinstance(self.currentState, str):
            self.compile_transition()
            try:
                NextState: str = self.config["TransitionTable"][self.currentState][
                    self.tape[self.pointer]
                ]
            except KeyError:
                self.printTransitions()
                return TuringResult.REJECTED, "".join(self.tape)

            [self.currentState, write, direction] = NextState.split(" ")
            # print(self.currentSate in self.config["FinalStates"])
            if not self.currentState or self.currentState == "":
                self.printTransitions()
                return TuringResult.REJECTED, "".join(self.tape)
            if self.currentState in self.config["FinalStates"]:
                self.printTransitions()
                return TuringResult.ACCEPTED, "".join(self.tape)
            self.tape[self.pointer] = write

            if direction == "R":
                self.increasePointer()
            elif direction == "L":
                self.decreasePointer()
            elif direction == "S":
                self.printTransitions()
                return TuringResult.ACCEPTED, "".join(self.tape)
            else:
                self.printTransitions()
                return ValueError(f"Invalid Direction `{direction}`: {self.__repr__()}")
        return ValueError("Infinite Loop")
