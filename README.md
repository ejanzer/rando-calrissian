# March Madness (Weighted) Random Pick Generator aka Rando Calrissian

## Usage

1. Clone the repo.
2. Download the NCAA forecasts from fivethirtyeight.com as a csv.
3. `cd rando-calrissian` and run: `python3 rando/picker.py ~/path/to/fivethirtyeight_ncaa_forecasts.csv`
4. The script will ask you to confirm the winners of play-in matches. Press the number corresponding to the team that won.
5. The script will show the first matchup and select a winner.
6. Enter the script's pick into your bracket builder of choice.
7. Press 'y' (or enter, or any key that's not 'n') to confirm and move on to the next matchup.
8. Repeat 4-7 until your bracket is complete.

## Notes

- If you'd rather get the whole bracket at once, change the value of `confirm` to `False` in `picker.py` and say yes when it asks if you want to print the whole thing at the end.
- If you're not sure what it's doing, change the value of `verbose` to `True` in `picker.py` and it will print logs.
- Pressing 'n' when it asks you to confirm will exit the program. This might not be what you expect.

## TODO

- Enable passing in `--verbose` and `--confirm` as command line arguments instead of hard-coding the values.
- Probably should use pyenv for simpler setup.
- Allow "re-rolling" a pick when the user presses 'n' instead of just bailing out of the entire program.
- Add more helpful output formats for the final result, like csv.
