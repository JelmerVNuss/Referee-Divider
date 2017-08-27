class Team:
    def __init__(self, club, level):
        self.club = club
        self.level = level

    def __str__(self):
        return "{} {}".format(self.club, self.level)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False
