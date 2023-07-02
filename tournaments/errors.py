class WrongAmountTeamsError(Exception):
    def __init__(self, stage_name):
        self.stage_name = stage_name

    def __str__(self):
        return f"На стадии {self.stage_name} неверное кол-во команд участников"


class NoNextStageError(Exception):
    def __init__(self, stage_name):
        self.stage_name = stage_name

    def __str__(self):
        return f"Нельзя узнать следующую стадию у {self.stage_name}, так как это финал"
