import random
import os


def Main():
    Again = "y"
    Score = 0
    while Again == "y":  # If the user inputs something other than Again, stop the puzzle
        Filename = input("Press Enter to start a standard puzzle or enter name of the file to load: ")
        # ERROR: There is no check here to validate that the user has only pressed Enter, instead is checking solely
        # for the existence of an input.
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8,
                              int(8 * 8 * 0.6))  # (0.6) Constant to determine how many cells you can place symbols
            # into.
        Score = MyPuzzle.AttemptPuzzle()  # Create puzzle
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()  # Allows user to change Again from 'y'.


class Puzzle():
    def __init__(self, *args):
        """
            Name: __init__
            Parameters: self, *args (variable number of arguments)
            Datatype: Puzzle object, *args (tuple)
            Purpose: Initialize a Puzzle object. If one argument is provided, load a puzzle from a file; otherwise, create a new puzzle with a specified size and symbols.
            """

        if len(args) == 1:  # The following attributes are 'Private' i.e __
            # Create default arguments if no arguments are passed in
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []

            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:  # 10% of the time, create a blocked cell within the grid.
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)  # Adding the cell to the grid via list
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []

            # The string pattern 'QQ**Q**QQ' indicates that the puzzle follows a spiral motion for creating the
            # puzzle pattern.
            QPattern = Pattern("Q", "QQ**Q**QQ")
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

    def __repr__(self):
        """
            Name: __repr__
            Parameters: self
            Datatype: Puzzle object
            Purpose: Return a string representation of the Puzzle object's current state, including attributes like score, symbols left, grid size, and the grid itself.
            """
        return f"Puzzle(Score={self.__Score}, SymbolsLeft={self.__SymbolsLeft}, GridSize={self.__GridSize}, Grid={self.__Grid}, AllowedPatterns={self.__AllowedPatterns}, AllowedSymbols={self.__AllowedSymbols})"


def __LoadPuzzle(self, Filename):
    """
        Name: __LoadPuzzle
        Parameters: self, Filename (str)
        Datatype: Puzzle object, str
        Purpose: Load puzzle details from a file, including allowed symbols, patterns, grid size, and current state.

        """
    try:
        with open(Filename) as f:
            NoOfSymbols = int(f.readline().rstrip())
            for Count in range(1, NoOfSymbols + 1):
                self.__AllowedSymbols.append(f.readline().rstrip())
            NoOfPatterns = int(f.readline().rstrip())
            for Count in range(1, NoOfPatterns + 1):
                Items = f.readline().rstrip().split(",")
                P = Pattern(Items[0], Items[1])
                self.__AllowedPatterns.append(P)
            self.__GridSize = int(f.readline().rstrip())
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                Items = f.readline().rstrip().split(",")
                if Items[0] == "@":
                    C = BlockedCell()
                    self.__Grid.append(C)
                else:
                    C = Cell()
                    C.ChangeSymbolInCell(Items[0])
                    for CurrentSymbol in range(1, len(Items)):
                        C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                    self.__Grid.append(C)
            self.__Score = int(f.readline().rstrip())
            self.__SymbolsLeft = int(f.readline().rstrip())
    except:
        print("Puzzle not loaded")


def AttemptPuzzle(self):
    """
        Name: AttemptPuzzle
        Parameters: self
        Datatype: Puzzle object
        Purpose: Allow the user to attempt to solve the puzzle by entering symbols for grid cells. Return the final score.
        """

    Finished = False
    while not Finished:
        self.DisplayPuzzle()
        print("Current score: " + str(self.__Score))
        Row = -1
        Valid = False
        while not Valid:
            try:
                Row = int(input("Enter row number: "))
                Valid = True
            except:
                pass
        Column = -1
        Valid = False
        while not Valid:
            try:
                Column = int(input("Enter column number: "))
                Valid = True
            except:
                pass
        Symbol = self.__GetSymbolFromUser()
        self.__SymbolsLeft -= 1  # Deduct the amount of moves you have left
        CurrentCell = self.__GetCell(Row, Column)  # Refer to __GetCell()
        if CurrentCell.CheckSymbolAllowed(Symbol):
            CurrentCell.ChangeSymbolInCell(Symbol)
            AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
            if AmountToAddToScore > 0:
                self.__Score += AmountToAddToScore
        if self.__SymbolsLeft == 0:
            Finished = True
    print()
    self.DisplayPuzzle()
    print()
    return self.__Score


def __GetCell(self, Row, Column):
    """
        Name: __GetCell
        Parameters: self, Row (int), Column (int)
        Datatype: Puzzle object, int, int
        Purpose: Get the cell at the specified row and column in the puzzle grid.
        """

    Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
    if Index >= 0:
        return self.__Grid[Index]
    else:
        raise IndexError()


def CheckforMatchWithPattern(self, Row, Column):  # Testing purposes, start at Row 2 and Column 2
    """
        Name: CheckforMatchWithPattern
        Parameters: self, Row (int), Column (int)
        Datatype: Puzzle object, int, int
        Purpose: Check for matching patterns starting from the specified row and column. Update the puzzle state and return the score.
        """

    for StartRow in range(Row + 2, Row - 1, -1):  # Start at Row4, stop at Row1, steps in -1.
        for StartColumn in range(Column - 2, Column + 1):  # Start at column 0, and stop at Column 3.
            try:
                PatternString = ""
                PatternString += self.__GetCell(StartRow,
                                                StartColumn).GetSymbol()  # Using Row2 and Column2, it will start at 31st cell.
                PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                # Following the loop it will look in 40th Cell.
                PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                # Following this pattern, it will move to 49th cell. This means the loop is going through the grid at an increment of 9. This means that by the end of the StartRow and StartColumn it'll reach the 58th index.
                PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                for P in self.__AllowedPatterns:
                    CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                    if P.MatchesPattern(PatternString, CurrentSymbol):
                        self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                        self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                        return 10
            except:
                pass
    return 0


def __GetSymbolFromUser(self):
    """
        Name: __GetSymbolFromUser
        Parameters: self
        Datatype: Puzzle object
        Purpose: Prompt the user to enter a symbol and validate that it is allowed. Return the chosen symbol.
        """

    Symbol = ""
    while not Symbol in self.__AllowedSymbols:
        Symbol = input("Enter symbol: ")
    return Symbol


def __CreateHorizontalLine(self):
    """
       Name: __CreateHorizontalLine
       Parameters: self
       Datatype: Puzzle object
       Purpose: Create a horizontal line of dashes for displaying the puzzle grid.
       """

    Line = "  "
    for Count in range(1, self.__GridSize * 2 + 2):
        Line = Line + "-"

    return Line


def DisplayPuzzle(self):
    """
        Name: DisplayPuzzle
        Parameters: self
        Datatype: Puzzle object
        Purpose: Display the current state of the puzzle grid.
        """

    print()
    if self.__GridSize < 10:
        print("  ", end='')
        for Count in range(1, self.__GridSize + 1):
            print(" " + str(Count), end='')
    print()
    print(self.__CreateHorizontalLine())
    for Count in range(0, len(self.__Grid)):
        if Count % self.__GridSize == 0 and self.__GridSize < 10:
            print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
        print("|" + self.__Grid[Count].GetSymbol(), end='')
        if (Count + 1) % self.__GridSize == 0:
            print("|")
            print(self.__CreateHorizontalLine())


class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        """
            Name: __init__
            Parameters: self, SymbolToUse (str), PatternString (str)
            Datatype: Pattern object, str, str
            Purpose: Initialize a Pattern object with a symbol and a string pattern sequence.
            """

        self.__Symbol = SymbolToUse  # Q
        self.__PatternSequence = PatternString  # i.e QQ**Q**QQ

    def __repr__(self):
        return f"Pattern(Symbol: {self.__Symbol}, PatternSequence: {self.__PatternSequence})"

    def MatchesPattern(self, PatternString, SymbolPlaced):
        """
        Name: MatchesPattern Parameters: self, PatternString (str), SymbolPlaced (str) Datatype: Pattern object, str,
        str Purpose: Check if the provided pattern string matches the pattern sequence and the symbol placed in the
        grid cell.
        """
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0,
                           len(self.__PatternSequence)):  # length of pattern sequence = 3. Therefore, it's a loop
            # that'll count up from 0 - 9
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    def GetPatternSequence(self):
        """
            Name: GetPatternSequence
            Parameters: self
            Datatype: Pattern object
            Purpose: Return the pattern sequence associated with the pattern object.
            """

        return self.__PatternSequence


class Cell:
    def __init__(self):
        """
           Name: __init__
           Parameters: self
           Datatype: Cell object
           Purpose: Initialize a Cell object with an empty symbol and an empty list of disallowed symbols.
           """

        self._Symbol = ""
        self.__SymbolsNotAllowed = []


def GetSymbol(self):
    """
        Name: GetSymbol
        Parameters: self
        Datatype: Cell object
        Purpose: Return the symbol in the cell or a dash if the cell is empty.
        """
    if self.IsEmpty():
        return "-"
    else:
        return self._Symbol


def IsEmpty(self):
    """
        Name: IsEmpty
        Parameters: self
        Datatype: Cell object
        Purpose: Check if the cell is empty (does not contain a symbol).
        """
    if len(self._Symbol) == 0:
        return True
    else:
        return False


def ChangeSymbolInCell(self, NewSymbol):
    """
        Name: ChangeSymbolInCell
        Parameters: self, NewSymbol (str)
        Datatype: Cell object, str
        Purpose: Change the symbol in the cell to the specified new symbol.
        """
    self._Symbol = NewSymbol


def CheckSymbolAllowed(self, SymbolToCheck):
    """
        Name: CheckSymbolAllowed
        Parameters: self, SymbolToCheck (str)
        Datatype: Cell object, str
        Purpose: Check if the provided symbol is allowed in the cell based on the list of disallowed symbols.
        """

    for Item in self.__SymbolsNotAllowed:
        if Item == SymbolToCheck:
            return False
    return True


def AddToNotAllowedSymbols(self, SymbolToAdd):
    """
        Name: AddToNotAllowedSymbols
        Parameters: self, SymbolToAdd (str)
        Datatype: Cell object, str
        Purpose: Add the specified symbol to the list of disallowed symbols for the cell.
        """
    self.__SymbolsNotAllowed.append(SymbolToAdd)


def UpdateCell(self):
    """
        Name: UpdateCell
        Parameters: self
        Datatype: Cell object
        Purpose: Abstract method intended to be changed via a child class. (No specific implementation in this class.)
        """
    pass


class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        """
            Name: CheckSymbolAllowed
            Parameters: self, SymbolToCheck (str)
            Datatype: BlockedCell object, str
            Purpose: Override the CheckSymbolAllowed method to always return False since symbols are not allowed in a blocked cell.
            """
        return False


if __name__ == "__main__":
    # Main()
    pattern = Pattern("Q", "QQ**Q**QQ")
    print(pattern)
