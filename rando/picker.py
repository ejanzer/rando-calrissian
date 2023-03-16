import csv
import math
import random
import sys
import re

# TODO Figure out how to make these arguments
verbose = False 
confirm = True

class Team:
    def __init__(self, id, name, seed, region, probs):
        self.id = id
        self.name = name
        self.seed = parse_seed(seed)
        self.region = region
        self.probs = probs

    def __str__(self):
      return str(self.seed) + " " + self.name

seeds = [1, 16, 8, 9, 5, 12, 4, 13, 6, 11, 3, 14, 7, 10, 2, 15]
seed_to_index = {k:v for (k, v) in zip(seeds, range(0, 16))}

region_positions = ["upper left", "upper right", "lower left", "lower right"]

# Having this out here makes it possible to use the script in the REPL to make one-off picks
# (if you don't want to re-run your whole bracket)
teams = {}

def main():
    print("Which tournament are you making a bracket for, men's or women's? (M/w)")
    gender = "mens"
    if input() == "w":
        gender = "womens"

    regions = []
    # Put the regions in the proper order: upper left, upper right, lower left, lower right
    available_regions = ["West", "South", "East", "Midwest"]
    region_index = 0
    while region_index < 3:
      print("Which region is in the " + region_positions[region_index] + "?")
      for i in range(len(available_regions)):
        print(str(i + 1) + ". " + available_regions[i])
      selection = input()
      try:
        index = int(selection) - 1
        regions.append(available_regions.pop(index))
        region_index += 1
      except:
        print("Please enter a valid number.")
        continue

    # We don't need to ask for the last one
    regions.append(available_regions.pop())
    if verbose:
      print(regions)

    filename = sys.argv[1]

    bracket = [[] for i in range(0, 6)]

    # Initialize arrays for each region so that we can insert teams in the correct index
    last_round_picks = {}
    for region in regions:
      last_round_picks[region] = [None for i in range(0, 16)]

    with open(filename) as file:
        reader = csv.reader(file, delimiter=',')
        forecast_date = None
        for row in reader:

            # Skip the column headers row
            if row[1] == "forecast_date":
              continue
            elif forecast_date is None:
              forecast_date = row[1]
              print("Using forecast data from " + forecast_date)
            else:
              if forecast_date != row[1]:
                continue
          
            if row[0] != gender:
                # Exclude results from the other tournament.
                continue
            else:
                id = row[12]
                name = row[13]
                region = row[15]
                probs = row[4:10]
                seed = row[16]
                team = Team(id, name, seed, region, probs)
                teams[id] = team

                if not last_round_picks.get(region):
                  raise Exception("Invalid region: " + region)

                # This arranges the teams in the right order for matchups (1, 16, ..., 2, 15)
                index = seed_to_index[parse_seed(seed)]

                if last_round_picks[region][index] != None:
                  existing = last_round_picks[region][index]
                  print("Found two teams for the same seed. Which was the winner? 1/2")
                  print("1. " + teams[existing].name)
                  print("2. " + teams[id].name)
                  winner = input()
                  while winner not in ["1", "2"]:
                    print("Sorry, I didn't understand that. Please enter 1 or 2")
                    winner = input()
                  if winner == "1":
                    continue

                last_round_picks[region][index] = id

    round = 0
    while round < 4:
      num_teams = 64 // 2**round
      picks = make_picks_for_round(regions, round, num_teams, teams, last_round_picks)
      last_round_picks = picks
      for region in regions:
        bracket[round] += [teams[id].name for id in last_round_picks[region]]
      round += 1

    print("\nFinal Four")
    top_left = last_round_picks[regions[0]][0]
    bottom_left = last_round_picks[regions[2]][0]
    team_1 = make_pick(teams[top_left], teams[bottom_left], round)
    bracket[round].append(team_1.name)

    top_right = last_round_picks[regions[1]][0]
    bottom_right = last_round_picks[regions[3]][0]
    team_2 = make_pick(teams[top_right], teams[bottom_right], round)
    bracket[round].append(team_2.name)

    round += 1
    print("\nFinals")
    champion = make_pick(team_1, team_2, round)
    bracket[round].append(champion.name)
    print("And the winner is..." + champion.name + "!")

    print("Print full bracket? Y/n")
    confirm = input()
    if (confirm != "n"):
      for i in range(0, len(bracket)):
        print("Round " + str(i + 1))
        print("Picks:")
        print(bracket[i])

def make_picks_for_round(regions, round, num_teams, teams, last_round_picks):
    print("\nRound of " + str(num_teams))
    picks = {}
    for region in regions:
      picks[region] = []
      print("Now picking for region: " + region)
      teams_in_region = last_round_picks[region]
      if len(teams_in_region) != num_teams // 4:
        raise Exception("Insufficient picks from last round")

      # Match up first two picks, then next two, etc.
      matches = [match for match in zip(teams_in_region[0:len(teams_in_region):2], teams_in_region[1:len(teams_in_region):2])]
      for match in matches:
        id_1, id_2 = match
        team_1 = teams[id_1]
        team_2 = teams[id_2]
        winner = make_pick(team_1, team_2, round)

        if confirm:
          print("Ready to continue? (Y/n)")
          ready = input()
          if ready == "n":
            raise Exception("Abandon ship!")

        picks[region].append(winner.id)
    
    return picks

def make_pick(team_1, team_2, round):
  print(team_1)
  print(team_2)
  if verbose:
    print("Probabilities for round:")
  prob_1 = float(team_1.probs[round])
  prob_2 = float(team_2.probs[round])
  if verbose:
    print(team_1.name + ": " + str(prob_1))
    print(team_2.name + ": " + str(prob_2))

  if verbose:
    print("Expected point values: ")
  epv_1 = expected_point_value(
      round, prob_1, team_1.seed, team_2.seed)
  if verbose:
    print(team_1.name + ": " + str(epv_1))
  epv_2 = expected_point_value(
      round, prob_2, team_2.seed, team_1.seed)
  if verbose:
    print(team_2.name + ": " + str(epv_2))

  winner = trial(team_1, epv_1, team_2, epv_2)
  print("Your pick is: " + winner.name)
  return winner


def expected_point_value(round, prob, seed, other_seed):
    base = math.pow(2, round)
    score = base + seed_differential(seed, other_seed)
    return prob * score


def parse_seed(seed):
    try:
        return int(seed)
    except ValueError:
        # Apparently seeds can be "11a", "11b", etc., whatever that means.
        match = re.search(r'(\d+)[ab]', seed)
        if match:
            return int(match.group(1))


def seed_differential(one, two):
    return one - two if one - two > 0 else 0


def trial(team_1, epv_1, team_2, epv_2):
    boundary = epv_1 / (epv_1 + epv_2)
    if verbose:
      print("Probability for team 1:  " + str(boundary))
    rand = random.uniform(0, 1)
    if verbose:
      print("Random number: " + str(rand))
    return team_1 if rand < boundary else team_2


if __name__ == "__main__":
    main()
