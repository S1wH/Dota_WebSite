class EmptyMatchPeriodError(Exception):
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return f'У сыгранного матча {self.id} должны быть периоды'
