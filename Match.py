from config import CLUB_NAME


class Match:
    def __init__(self, homeTeam, awayTeam, meetingDateTime, startDateTime, endDateTime, returnedDateTime, referee):
        self.homeTeam = homeTeam
        self.awayTeam = awayTeam
        self.meetingDateTime = meetingDateTime
        self.startDateTime = startDateTime
        self.endDateTime = endDateTime
        self.returnedDateTime = returnedDateTime
        # There is no return needed in a home match.
        if homeTeam.club == CLUB_NAME:
            self.returnedDateTime = endDateTime
        self.referee = referee

    def __str__(self):
        return "{} - {} on {} from {} to {} with referee {}".format(self.homeTeam,
                                                                    self.awayTeam,
                                                                    self.startDateTime.date(),
                                                                    self.startDateTime.time(),
                                                                    self.endDateTime.time(),
                                                                    self.referee.name)

    def getMinutesMatchesOverlap(self, otherMatch):
        delta = min(self.returnedDateTime, otherMatch.returnedDateTime) - max(self.meetingDateTime, otherMatch.meetingDateTime)
        if delta.total_seconds() < 0:
            minutesOverlap = 0
        else:
            minutesOverlap = delta.total_seconds() / 60.0
        return minutesOverlap

    def doesOverlapWith(self, otherMatch):
        return self.getMinutesMatchesOverlap(otherMatch) > 0
