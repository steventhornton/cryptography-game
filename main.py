#!/usr/bin/env python3

import json
import numpy as np
import pandas as pd
import random
from hashlib import sha3_256

pd.set_option('max_colwidth', None)
pd.set_option('display.max_rows', 500)

# Range to select numbers from
NUM_RANGE = [0, 100]


def generate_private_key(nbits: int = 256) -> int:
    return random.getrandbits(nbits)


def hash_function(x: int) -> int:
    h = sha3_256()
    h.update(str(x).encode('utf-8'))
    return int(h.hexdigest(), base=16)


def play_game():
    k = generate_private_key()
    print(f"Your private key is {k}")

    while True:

        valid_input = False
        while not valid_input:

            print(f"Pick a number between {NUM_RANGE[0]} and {NUM_RANGE[1]}: ", end='')
            x = input()

            # Check if the input was an integer
            try:
                x = int(x)
            except ValueError:
                print(f"Ensure you input an integer! Pick again...")
                continue

            # Check if value is in the valid range
            if NUM_RANGE[0] <= x <= NUM_RANGE[1]:
                valid_input = True
            else:
                print(f"Input value should be between {NUM_RANGE[0]} and {NUM_RANGE[1]}! Pick again...")

        # Hash
        y = (x + 1) * k
        y_prime = hash_function(y)

        print(f"Submit your prediction: {y_prime}")


def determine_winner():

    with open('player_keys.json') as f:
        player_keys = json.load(f)

    df = pd.read_csv('predictions.csv', dtype = {'Timestamp': object, 'Submit your value': object})
    df.rename(columns={'Submit your value': 'prediction_hash'}, inplace=True)

    df_cj = pd.DataFrame(
        [[player, prediction, str(hash_function(int(key) * int(prediction + 1)))] for player, key in player_keys.items() for prediction in np.arange(NUM_RANGE[0], NUM_RANGE[1] + 1)],
        columns=['player', 'prediction', 'prediction_hash']
    )

    df = df.merge(df_cj, on='prediction_hash', how='left')

    average_guess = df['prediction'].mean()
    print(f"Average Guess: {average_guess}")

    # Distance from 2/3 of average guess
    df['distance'] = df.apply(lambda row: abs(row['prediction'] - (2/3) * average_guess), axis=1)
    df = df.sort_values(by=['distance'])

    print(df.to_string(index=False))


if __name__ == '__main__':
    play_game()
    # determine_winner()
