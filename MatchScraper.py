import urllib.request
from datetime import datetime, timedelta

from bs4 import BeautifulSoup


from Team import Team
from Match import Match
from Referee import Referee


MATCH_URL = "http://www.eemvogels.nl/competitie/wedstrijdprogramma"
MATCH_DURATION = timedelta(hours=1)


class MatchScraper:
    def __init__(self):
        pass

    def scrapeMatches(self):
        matches = []

        page = urllib.request.urlopen(MATCH_URL)
        soup = BeautifulSoup(page, 'html.parser')

        rows = self.findMatchRows(soup)
        for row in rows:
            match = self.scrapeMatchFromRow(row)
            matches.append(match)

        return matches


    def findMatchRows(self, page):
        rows = page.findAll('table', {'id': 'programma'})[0].findAll('tbody')[0].findAll('tr')
        return rows


    def scrapeMatchFromRow(self, row):
        data = row.findAll('td')

        homeClub, homeLevel = getClubAndLevelFromTeamName(data[1].text)
        awayClub, awayLevel = getClubAndLevelFromTeamName(data[2].text)
        homeTeam = Team(homeClub, homeLevel)
        awayTeam = Team(awayClub, awayLevel)

        startDate = data[0].text
        startDate = datetime.strptime(startDate, '%d-%m-%Y').date()
        startTime = data[4].text
        startTime = datetime.strptime(startTime, '%H:%M').time()

        meetingTime = data[3].text
        meetingTime = datetime.strptime(meetingTime, '%H:%M').time()

        meetingDateTime = datetime.combine(startDate, meetingTime)
        startDateTime = datetime.combine(startDate, startTime)
        endDateTime = startDateTime + MATCH_DURATION
        # Assume that returning takes the same amount of time as the time between meeting and start of the match.
        returnedDateTime = endDateTime + (startDateTime - meetingDateTime)

        referee = Referee("Not Scheduled", "", "", "", "", "", [])
        match = Match(homeTeam, awayTeam, meetingDateTime, startDateTime, endDateTime, returnedDateTime, referee)
        return match


def getClubAndLevelFromTeamName(teamName):
    split = teamName.split(" ")
    club = " ".join(split[:-1])
    level = split[-1:][0]

    # Add a "S"enior to the level if there is only a number in the team level.
    if len(level) == 1:
        level = "S{}".format(level)

    return club, level
