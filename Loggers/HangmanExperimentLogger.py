import json
from datetime import datetime as dt


class HangmanLogger:
    """Custom logger for the experiment"""

    def __init__(self):
        self.__detail_logs_h = ["BotName", "SettingName", "SettingJson", "GameWord", "TotalGuessesMade", "LatestGameState", "GameResult"]
        self.__detail_logs = []

    def log(self, bot_name, setting_name, last_resp_json):
        self.__detail_logs.append(
            [
                bot_name,
                setting_name,
                json.dumps(last_resp_json["game_settings"]),
                json.dumps(last_resp_json["game_state"]["game_word"]),
                len(last_resp_json["game_state"]["correct_guesses"]) + len(last_resp_json["game_state"]["incorrect_guesses"]),
                json.dumps(last_resp_json["game_state"]),
                last_resp_json["outcome"]
            ]
        )

    def log_exception(self, setting_name, game_initalized_settings, exception_message):
        game_initalized_settings = game_initalized_settings
        self.__detail_logs.append(
            [
                "N/A",
                setting_name,
                json.dumps(game_initalized_settings),
                "N/A",
                "N/A",
                "N/A",
                f"Error: {exception_message}"
            ]
        )

    def export_logs(self):
        base_path = "Logs/"
        base_name = f"Exp.{dt.now():%Y_%m_%d_%H_%M_%S}"

        # Export details
        self.export(base_path + base_name + ".Details.tsv", self.__detail_logs_h, self.__detail_logs)

        # Export skill summary per bot
        skill_summary_h, skil_summary_d = self.get_skill_summary()
        self.export(base_path + base_name + ".SkillSummary.tsv", skill_summary_h, skil_summary_d)

    def get_skill_summary(self):
        iBotName = self.__detail_logs_h.index("BotName")
        iSettingName = self.__detail_logs_h.index("SettingName")
        iGameResult = self.__detail_logs_h.index("GameResult")
        skill_sum_logs_h = ["BotName", "GameSettingTypeName", "GameWinRate"]
        skill_sum_logs_d = []

        game_counts = dict()
        for row in self.__detail_logs:
            if "Error" in row[iGameResult]:
                continue

            key = row[iBotName] + row[iSettingName]
            result = row[iGameResult]
            if key not in game_counts:
                game_counts[key] = {"win": 0, "lose": 0}
                skill_sum_logs_d.append([row[iBotName], row[iSettingName], ""])
            game_counts[key][result] += 1

        for row in skill_sum_logs_d:
            key = row[0] + row[1]
            win_count = game_counts[key]["win"]
            lose_count = game_counts[key]["lose"]
            total_count = win_count + lose_count
            row[-1] = f"{win_count / total_count * 100}% ({win_count}/{total_count})"
        return skill_sum_logs_h, skill_sum_logs_d

    @staticmethod
    def export(file, header, data):
        f = open(file, 'w', encoding='utf-8')
        for row in [header] + data:
            f.write('\t'.join(map(str, row)) + '\n')
