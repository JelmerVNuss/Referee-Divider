class Referee:
    def __init__(self, name, email, team, coachTeam, diplom, levelRange, preferences):
        self.name = name
        self.email = email
        self.team = team
        self.coachTeam = coachTeam
        self.diplom = diplom
        self.levelRange = levelRange
        self.preferences = preferences

    def __str__(self):
        return "{} ({}) from {} (coach of {}) with diplom {} can referee {} with preferences {}".format(
            self.name,
            self.email,
            self.team,
            self.coachTeam,
            self.diplom,
            self.levelRange,
            self.preferences
        )

    def ownMatches(self, allMatches):
        def mustPlayOrCoach(match):
            return self.team == match.homeTeam or self.team == match.awayTeam or self.coachTeam == match.homeTeam or self.coachTeam == match.awayTeam
        return [match for match in allMatches if mustPlayOrCoach(match)]

    def canRefereeMatch(self, match, allMatches):
        if match.homeTeam.level not in self.levelRange:
            return False
        for ownMatch in self.ownMatches(allMatches):
            if ownMatch.doesOverlapWith(match):
                return False
        else:
            return True
