import random
from enum import Enum
from nltk.corpus import words


class Hangman:
    """Hangman game-play api"""

    class Settings(Enum):
        lower = "WordLengthLowerBound"
        upper = "WordLengthUpperBound"
        guesses = "TotalGuessesAllowed"

    class __ApiEnums(Enum):
        outcome = "outcome"
        letter = "letter"
        request = "request"
        game_state = "game_state"
        game_settings = "game_settings"
        win = "win"
        lose = "lose"
        correct = "correct"
        incorrect = "incorrect"
        game_word = "game_word"
        current_state = "current_state"
        guesses_left = "guesses_left"
        correct_guesses = "correct_guesses"
        incorrect_guesses = "incorrect_guesses"

    def __init__(self, settings=None):
        # Default settings
        self.settings = {
            self.Settings.lower: float("inf") * -1,
            self.Settings.upper: float("inf"),
            self.Settings.guesses: 10
        }

        # Apply external settings
        if settings is not None:
            for i in self.settings:
                if i in settings:
                    self.settings[i] = settings[i]

        self.__the_word_str = ""
        self.__the_word = dict()
        self.__guessed_correct = list()
        self.__guessed_incorrect = list()
        self.__the_word_length = int()
        self.__corpus = list()
        self.__guesses_left = self.settings[self.Settings.guesses]
        self.__game_on = True
        self.__get_corpus()
        self.__pick_a_random_word()

    # TODO: Implement a restart method for the game to restart it with the same word

    # Game prep
    def __pick_a_random_word(self):
        word_pool = [word for word in self.__corpus if self.settings[self.Settings.upper] >= len(word) >= self.settings[self.Settings.lower]]
        if not word_pool:
            raise ValueError("No game created for given settings!")

        self.__the_word_str = random.choice(word_pool)
        for i, letter in enumerate(self.__the_word_str):
            if letter not in self.__the_word:
                self.__the_word[letter] = list()
            self.__the_word[letter].append(i)
        self.__the_word_length = len(self.__the_word_str)

    def __get_corpus(self):
        all_words = words.words()[:10]
        self.__corpus = {word.upper() for word in all_words}

    # API stuff
    def post(self, req_json):
        if not self.__game_on:
            raise Exception("Game is finished")
        guessed_letter = req_json["letter"]
        status_json = self.__play_a_turn(guessed_letter)
        resp_json = self.__create_resp_json(status_json)
        return self.__response_serializer(resp_json)

    def get(self, req_json):
        if req_json["request"] == "game_state":
            resp_json = self.__response_serializer(self.__get_game_state())
        elif req_json["request"] == "game_word":
            resp_json = self.__get_the_game_word()
        else:
            raise ValueError("Bad request!")
        return self.__response_serializer(resp_json)

    # Game play
    def __play_a_turn(self, letter):
        status = self.__guess_a_letter(letter)
        return {self.__ApiEnums.outcome: status, self.__ApiEnums.letter: letter}

    def __guess_a_letter(self, letter):
        if letter in self.__the_word:
            self.__guessed_correct.append(letter)
            status = self.__ApiEnums.correct
        else:
            self.__guessed_incorrect.append(letter)
            status = self.__ApiEnums.incorrect
        self.__guesses_left -= 1
        return status

    # Helpers
    def __create_resp_json(self, status_json):
        # Get status
        if len(set(self.__the_word.keys()).difference(self.__guessed_correct)) == 0:
            self.__game_on = False
            status_json[self.__ApiEnums.outcome] = self.__ApiEnums.win
        elif self.__guesses_left == 0:
            self.__game_on = False
            status_json[self.__ApiEnums.outcome] = self.__ApiEnums.lose
        else:
            # Game continues
            pass

        # Get settings
        status_json[self.__ApiEnums.game_settings] = self.settings

        # Get state
        status_json[self.__ApiEnums.game_state] = self.__get_game_state()

        return status_json

    def __get_game_state(self):
        game_state = {
            self.__ApiEnums.current_state: self.__get_current_state_of_the_word(),
            self.__ApiEnums.guesses_left: self.__guesses_left,
            self.__ApiEnums.correct_guesses: self.__guessed_correct,
            self.__ApiEnums.incorrect_guesses: self.__guessed_incorrect
        }

        if not self.__game_on:
            game_state[self.__ApiEnums.game_word] = self.__get_the_game_word()

        return game_state

    def __get_the_game_word(self):
        if self.__game_on:
            raise OverflowError("Cannot request the game word if game is still on!")

        game_word = {
            self.__ApiEnums.game_word: self.__the_word_str
        }
        return game_word

    def __get_current_state_of_the_word(self):
        current_state = ["_"] * len(self.__the_word_str)
        for letter in self.__guessed_correct:
            for i in self.__the_word[letter]:
                current_state[i] = letter
        return " ".join(current_state)

    def __response_serializer(self, resp_json):
        new_resp_json = dict()
        for key, val in resp_json.items():
            # If val is dict convert recursively
            if isinstance(val, dict):
                val = self.__response_serializer(val)

            if isinstance(val, float) and (val == float('inf') or val == float('inf') * -1):
                val = None

            if isinstance(val, Enum):
                val = val.value

            # If key is not str make it str
            if isinstance(key, Enum):
                key = key.value

            new_resp_json[key] = val
        return new_resp_json
