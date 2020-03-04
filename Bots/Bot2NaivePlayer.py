class NaivePlayer:
    """Random guess bot with no intelligence"""

    def __init__(self):
        freq_sorted_alphabet = [
            "E",
            "T",
            "A",
            "O",
            "I",
            "N",
            "S",
            "H",
            "R",
            "D",
            "L",
            "U",
            "W",
            "M",
            "F",
            "C",
            "G",
            "Y",
            "P",
            "B",
            "K",
            "V",
            "J",
            "X",
            "Q",
            "Z"
        ]
        self.__next_guess_generator = (letter for letter in freq_sorted_alphabet)

    def guess(self, _):
        # TODO: Implement a stateless bot
        return next(self.__next_guess_generator)
