from copy import deepcopy

from Bots.Bot1RandomPlayer import RandomPlayer
from Bots.Bot2NaivePlayer import NaivePlayer
from GamePlay.HangmanGameAPI import Hangman
from Loggers.HangmanExperimentLogger import HangmanLogger


def settings_serializer(resp_json):
    new_resp_json = dict()
    for key, val in resp_json.items():
        # If key is not str make it str
        if isinstance(key, Hangman.Settings):
            key = key.value

        new_resp_json[key] = val
    return new_resp_json


def play(game, bot):
    while True:
        guessed_letter = bot.guess(game)
        resp_json = game.post({"letter": guessed_letter})
        result = resp_json["outcome"]
        if result == "win" or result == "lose":
            break
    return resp_json


def main():
    settings = {
        "Default": dict(),
        "ShortWords(1-6 letters)": {
            Hangman.Settings.lower: 0,
            Hangman.Settings.upper: 5
        },
        "ShortWords20Guesses(1-6 letters)": {
            Hangman.Settings.lower: 0,
            Hangman.Settings.upper: 5,
            Hangman.Settings.guesses: 20
        },
        "LongWords(7-12 letters)": {
            Hangman.Settings.lower: 6,
            Hangman.Settings.upper: 11
        }
    }
    bots = {
        "BasicRandomBot": RandomPlayer(),
        "NaiveFreqBot": NaivePlayer()
    }
    sample_size = 1000
    logger = HangmanLogger()
    for setting_name, setting in settings.items():
        for i in range(sample_size):
            print(f"Running Exp for Game {setting_name}...")
            if i % 100 == 0:
                print(f"\t{i} out of {sample_size} are done...")
            game = Hangman(setting)
            for bot_name, bot in bots.items():
                _game = deepcopy(game)
                _bot = deepcopy(bot)
                last_resp_json = play(_game, _bot)
                logger.log(bot_name, setting_name, settings_serializer(last_resp_json))

    logger.export_logs()


if __name__ == '__main__':
    main()
