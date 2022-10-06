# Cryptography Game

## Setup
The game uses the following setup:
- Each player can make as many guesses as they would like
- Each player begins by generating a random 256-bit private key `K`.
- A player makes a guess within the supported range (0-100) and submits their hashed guess as:
  - Let `x` be the guess
  - Compute `y = (x + 1) * K`
  - Let `y' = hash(y)` where `hash` is the `sha3` hashing algorithm with 256 bits
  - Submit `y'`

The `play_game` function will generate a private key for the player and will allow them to make as many guesses as they would like.

## Example
- The `predictions.csv` file contains example predictions that have been submitted by players.
- The `player_keys.json` file contains the players private keys (this would not be revealed until after the game completed)
- The `determine_winner` function in `main.py` can be used to determine the winner given `predictions.csv` and `player_keys.json`
