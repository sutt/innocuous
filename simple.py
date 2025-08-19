
def demo():
    byte_values = bytes([13, 17])   # same as b'\x0d'
    print("Len of bytes:", len(byte_values))
    print("As bytes:", byte_values)

    for i in range(len(byte_values)):
        # Get its integer representation
        int_value = byte_values[i]
        print("As integer:", int_value)

        # Print in binary with 8 bits
        binary_str = format(int_value, "08b")
        print("As binary string:", binary_str)

        # Convert to a string encoding (base64 or hex is common)
        hex_str = bytes([byte_values[i]]).hex()
        print("As hex string:", hex_str)

# demo()

import random
import json
import math

SECRET_MESSAGE = bytes([13, 17])

N_TRIALS = 20
N_CHOICES = 10
A_TOTAL = 1.1
B_TOTAL = 1.3

selections = []
for _ in range(N_TRIALS):
    vals = [random.random() for _ in range(N_CHOICES)]
    vals = sorted(vals, reverse=True)
    choices = {i:v for i,v in enumerate(vals)}
    exps = [math.exp(v) for v in choices.values()]
    sum_exps = sum(exps)
    sum_exps = sum_exps * random.uniform(A_TOTAL, B_TOTAL)
    selections.append({k: v / sum_exps for k, v in zip(choices.keys(), exps)})

# check that all values in each dict sum to around 0.7 - 0.9
# check = [sum(e.values()) for e in selections]
# print(json.dumps(check, indent=2))

# TODO - encode the secret message by sampling the selections items 
# to produce a sequence of chars which represent the secret message
# based on the idea that selections is static and will be known at
# encode and decode time

