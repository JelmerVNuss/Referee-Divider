import json

from Team import Team
from Referee import Referee
from MatchScraper import MatchScraper

from config import CLUB_NAME, REFEREES_JSON


def loadReferees(filepath):
    referees = []
    with open(filepath, 'r') as f:
        data = json.load(f)
        for refereeInformation in data:
            name = refereeInformation["name"]
            email = refereeInformation["email"]
            team = Team(CLUB_NAME, refereeInformation["team"])
            coachTeam = Team(CLUB_NAME, refereeInformation["coachTeam"])
            diplom = refereeInformation["diplom"]
            levelRange = refereeInformation["levelRange"]
            preferences = refereeInformation["preferences"]

            referee = Referee(name, email, team, coachTeam, diplom, levelRange, preferences)
            referees.append(referee)
    return referees

referees = loadReferees(REFEREES_JSON)
print(referees[0])


matchScraper = MatchScraper()
matches = matchScraper.scrapeMatches()


print(referees[0].canRefereeMatch(matches[0], matches))

toScheduleMatches = [match for match in matches if match.homeTeam.club == CLUB_NAME and not match.homeTeam.level == "S1"]
print(len(toScheduleMatches))

possibleMatches = {}
for referee in referees:
    possibleMatches[referee] = []
    for match in toScheduleMatches:
        if referee.canRefereeMatch(match, matches):
            possibleMatches[referee].append(match)

onlyPreferredMatches = {}
for referee in referees:
    onlyPreferredMatches[referee] = []
    for match in possibleMatches[referee]:
        if match.homeTeam.level in referee.preferences:
            onlyPreferredMatches[referee].append(match)

# for referee in referees:
#     print(referee.name)
#     print("possible matches")
#     for p in possibleMatches[referee]:
#         print(p)
#     print("preferred matches only")
#     for p in onlyPreferredMatches[referee]:
#         print(p)


matchesCoveredInPossibleMatches = set()
for referee in referees:
    for match in possibleMatches[referee]:
        matchesCoveredInPossibleMatches.add(match)
matchesNotCoveredInPossibleMatches = set(toScheduleMatches) - matchesCoveredInPossibleMatches

matchesCoveredInPreferredMatches = set()
for referee in referees:
    for match in onlyPreferredMatches[referee]:
        matchesCoveredInPreferredMatches.add(match)
matchesNotCoveredInPreferredMatches = set(toScheduleMatches) - matchesCoveredInPreferredMatches

# print("Not covered in possible matches:")
# for match in matchesNotCoveredInPossibleMatches:
#     print(match)
# print("Not covered in preferred matches:")
# for match in matchesNotCoveredInPreferredMatches:
#     print(match)

# print("available referees per match")
# for match in toScheduleMatches:
#     print(match)
#     for referee in referees:
#         if match in onlyPreferredMatches[referee]:
#             print(referee.name)

print("available referees per match")
for match in toScheduleMatches:
    print(match)
    for referee in referees:
        if match in possibleMatches[referee]:
            print(referee.name)
