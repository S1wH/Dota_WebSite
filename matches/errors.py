class EmptyMatchPeriodError(Exception):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f'У сыгранного матча {self.id} должны быть периоды'


class MatchNotfound(Exception):
    def __init__(self, team1, team2, stage):
        self.team1 = team1
        self.team2 = team2
        self.stage = stage

    def __str__(self):
        return f'Не найден матч между командами {self.team1} и {self.team2} на стадии {self.stage}'
