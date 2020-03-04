import random


class RandomPlayer:
    """Random guess bot with no intelligence"""

    def __init__(self):
        self.__letter_pool = set(map(lambda x: chr(ord("A") + x), range(26)))

    def guess(self, game):
        game_state = game.get({"request": "game_state"})
        correct_guesses = game_state["correct_guesses"]
        incorrect_guesses = game_state["incorrect_guesses"]
        old_guesses = set(correct_guesses + incorrect_guesses)
        available_guesses = self.__letter_pool.difference(old_guesses)
        return random.choice(list(available_guesses))
