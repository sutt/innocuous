
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

selections = []
for _ in range(N_TRIALS):
    choices = {i: random.random() for i in range(N_CHOICES)}
    exps = [math.exp(v) for v in choices.values()]
    sum_exps = sum(exps)
    selections.append({k: v / sum_exps for k, v in zip(choices.keys(), exps)})

print(json.dumps(selections, indent=2))
