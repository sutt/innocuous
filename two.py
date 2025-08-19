import random, json, math, decimal
from decimal import Decimal, ROUND_FLOOR

decimal.getcontext().prec = 400  # bump if you encode many bytes

SECRET_MESSAGE = bytes([13, 17])

N_TRIALS = 5         # increase if you need more capacity
N_CHOICES = 10
A_TOTAL = 1.1
B_TOTAL = 1.3

# ----- build your selections (as in your code) -----
selections = []
for _ in range(N_TRIALS):
    vals = [random.random() for _ in range(N_CHOICES)]
    vals = sorted(vals, reverse=True)
    choices = {i: v for i, v in enumerate(vals)}
    exps = [math.exp(v) for v in choices.values()]
    sum_exps = sum(exps)
    sum_exps *= random.uniform(A_TOTAL, B_TOTAL)
    selections.append({k: v / sum_exps for k, v in zip(choices.keys(), exps)})

# ----- helpers -----
def _norm_probs(dist):
    # Normalize dict of {idx: weight} so probs sum to 1 (as Decimals), return (keys, probs, cums)
    keys = sorted(dist.keys())
    probs = [Decimal(dist[k]) for k in keys]
    s = sum(probs)
    # guard tiny rounding: if s==0, spread uniform
    if s == 0:
        probs = [Decimal(1) / Decimal(len(keys)) for _ in keys]
    else:
        probs = [p / s for p in probs]
    cums = []
    acc = Decimal(0)
    for p in probs:
        cums.append(acc)
        acc += p
    # ensure last bin closes at 1.0
    return keys, probs, cums

def _bytes_to_fraction(b: bytes):
    nbits = 8 * len(b)
    N = int.from_bytes(b, "big", signed=False)
    pow2 = 1 << nbits                     # integer 2**nbits
    denom = Decimal(pow2)                 # convert to Decimal
    # Center in the bin to avoid boundary issues
    x = (Decimal(N) + Decimal("0.5")) / denom
    return x, nbits

def _fraction_to_bytes(x: Decimal, nbits: int) -> bytes:
    # clamp to [0, 1 - 1/2^nbits]
    pow2 = 1 << nbits
    one = Decimal(1)
    eps = one / Decimal(pow2)
    if x < 0: 
        x = Decimal(0)
    if x >= 1:
        x = one - eps

    N = int((x * Decimal(pow2)).to_integral_value(rounding=ROUND_FLOOR))
    nbytes = (nbits + 7) // 8
    return N.to_bytes(nbytes, "big", signed=False)

# ----- encode -----
def encode_indices(msg: bytes, selections):
    x, nbits = _bytes_to_fraction(msg)  # x in [0,1)
    indices = []
    for dist in selections:
        keys, probs, cums = _norm_probs(dist)
        # find bin containing x
        chosen = None
        for i, (lo, p) in enumerate(zip(cums, probs)):
            hi = lo + p
            # include right edge only on last bin to avoid gaps
            if (x >= lo and x < hi) or (i == len(probs) - 1 and x >= lo and x <= hi):
                chosen = i
                # renormalize x within the chosen bin
                if p > 0:
                    x = (x - lo) / p
                else:
                    x = Decimal(0)
                indices.append(keys[i])
                break
        if chosen is None:
            # extremely rare numeric edge; fall back to last
            i = len(probs) - 1
            indices.append(keys[i])
            x = Decimal(0)
    return indices

# ----- decode -----
def decode_indices(indices, selections, out_nbytes):
    x = Decimal(0)
    for ind, dist in zip(indices, selections):
        keys, probs, cums = _norm_probs(dist)
        j = keys.index(ind)
        lo = cums[j]
        p = probs[j]
        x = lo + p * x
    return _fraction_to_bytes(x, 8 * out_nbytes)

# ----- demo -----
# print(json.dumps(selections, indent=2))
indices = encode_indices(SECRET_MESSAGE, selections)
recovered = decode_indices(indices, selections, out_nbytes=len(SECRET_MESSAGE))

print("Encoded indices:", indices)
print("Recovered bytes:", list(recovered))
print("OK?", recovered == SECRET_MESSAGE)
