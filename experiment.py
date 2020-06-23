from Bots.Bot1RandomPlayer import RandomPlayer
from Bots.Bot2NaivePlayer import NaivePlayer
from GamePlay.HangmanGameAPI import Hangman
from Loggers.HangmanExperimentLogger import HangmanLogger


class Experiment:

    def __init__(self, settings, bots, logger, sample_size):
        self.settings = settings
        self.bots = bots
        self.logger = logger
        self.sample_size = sample_size

    def Run(self):
        for setting_name, setting in self.settings.items():
            print(f"Running Exp for Game {setting_name}...")
            for i in range(self.sample_size):
                if i > 1 and i % 100 == 0:
                    print(f"\t{i} out of {self.sample_size} are done...")
                for bot_name, bot in self.bots.items():
                    game = Hangman(setting)
                    bot = bot()
                    last_resp_json = self.play(game, bot)
                    self.logger.log(bot_name, setting_name, last_resp_json)
        self.logger.export_logs()

    @staticmethod
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

    # TODO: Make bots restartable
    bots = {
        "BasicRandomBot": RandomPlayer,
        "NaiveFreqBot": NaivePlayer
    }

    logger = HangmanLogger()

    experiment = Experiment(settings, bots, logger, 1000)
    experiment.Run()


if __name__ == '__main__':
    main()
