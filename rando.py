import csv
import math
import random
import sys

class Team:
    def __init__(self, id, name, seed, region, probs):
        self.id = id
        self.name = name
        self.seed = int(seed)
        self.region = region
        self.probs = probs

def main():
    teams = {}
    filename = sys.argv[1]
    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        line = 0
        for row in reader:
            if line == 0:
                line += 1
                continue
            else:
                id = row[12]
                name = row[13]
                region = row[15]
                probs = row[4:10]
                seed = row[16]
                team = Team(id, name, seed, region, probs)
                teams[id] = team
                line += 1

    total_teams = 64
    round = 0
    print "Total number of teams: " + str(total_teams)

    # Everything below will be in loop

    # 5 rounds total
    while round < 6:
        print "Round #: " + str(round + 1)
        picks_to_make = int(total_teams / (math.pow(2, round)) / 2)
        print "Picks to make for round: " + str(picks_to_make)

        while picks_to_make > 0:
            print "Picks remaining: " + str(picks_to_make)

            print "Enter team ids"
            id_1 = raw_input()
            id_2 = raw_input()

            team_1 = teams[id_1]
            team_2 = teams[id_2]
            print "Team 1: " + team_1.name
            print "Team 2: " + team_2.name

            print "Probabilities for round:"
            prob_1 = float(team_1.probs[round])
            prob_2 = float(team_2.probs[round])
            print team_1.name + ": " + str(prob_1)
            print team_2.name + ": " + str(prob_2)

            print "Expected point values: "
            epv_1 = expected_point_value(round, prob_1, team_1.seed, team_2.seed)
            print team_1.name + ": " + str(epv_1)
            epv_2 = expected_point_value(round, prob_2, team_2.seed, team_1.seed)
            print team_2.name + ": " + str(epv_2)

            trial(team_1, epv_1, team_2, epv_2)

            print "Ok? Y/n"
            confirm = raw_input()
            if confirm != "n":
                picks_to_make -= 1

        # Increment the round
        print "Ok to move on to the next round? Y/n"
        confirm = raw_input()
        if confirm != "n":
            round += 1

def expected_point_value(round, prob, seed, other_seed):
    base = math.pow(2, round)
    score = base + seed_differential(seed, other_seed)
    return prob * score

def seed_differential(one, two):
    return one - two if one - two > 0 else 0

def trial(team_1, epv_1, team_2, epv_2):
    boundary = epv_1 / (epv_1 + epv_2)
    print "Probability for team 1:  " + str(boundary)
    rand = random.uniform(0, 1)
    print "Random number: " + str(rand)
    print "The pick is: " + team_1.name if rand < boundary else team_2.name

if __name__ == "__main__":
    main()
