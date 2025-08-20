import numpy as np

SECRET_MESSAGE = bytes([13, 17])

N_TRIALS = 5         # increase if you need more capacity
N_CHOICES = 10
A_TOTAL = 1.1
B_TOTAL = 1.3

# ----- build your selections (as in your code) -----
selections = []
for _ in range(N_TRIALS):
    vals = np.random.rand(N_CHOICES)
    vals = np.sort(vals)[::-1]
    exps = np.exp(vals)
    sum_exps = np.sum(exps)
    sum_exps *= np.random.uniform(A_TOTAL, B_TOTAL)
    probs = exps / sum_exps
    selections.append({i: v for i, v in enumerate(probs)})

# ----- helpers -----
def _norm_probs(dist):
    # Normalize dict of {idx: weight} so probs sum to 1, return (keys, probs, cums)
    keys = sorted(dist.keys())
    probs = np.array([dist[k] for k in keys], dtype=np.float64)
    s = np.sum(probs)
    # guard tiny rounding: if s==0, spread uniform
    if s == 0:
        probs = np.full(len(keys), 1.0 / len(keys))
    else:
        probs = probs / s
    cums = np.insert(np.cumsum(probs), 0, 0)[:-1]
    return keys, probs, cums

def _bytes_to_fraction(b: bytes):
    nbits = 8 * len(b)
    N = int.from_bytes(b, "big", signed=False)
    pow2 = 1 << nbits                     # integer 2**nbits
    # Center in the bin to avoid boundary issues
    x = (N + 0.5) / pow2
    return x, nbits

def _fraction_to_bytes(x: float, nbits: int) -> bytes:
    # clamp to [0, 1 - 1/2^nbits]
    pow2 = 1 << nbits
    eps = 1.0 / pow2
    if x < 0: 
        x = 0.0
    if x >= 1:
        x = 1.0 - eps

    N = int(np.floor(x * pow2))
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
                    x = 0.0
                indices.append(keys[i])
                break
        if chosen is None:
            # extremely rare numeric edge; fall back to last
            i = len(probs) - 1
            indices.append(keys[i])
            x = 0.0
    return indices

# ----- decode -----
def decode_indices(indices, selections, out_nbytes):
    x = 0.0
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
