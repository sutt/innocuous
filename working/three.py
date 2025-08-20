import random
import math
import decimal
from decimal import Decimal, ROUND_FLOOR

# ----------------------------
# Config / Demo payload
# ----------------------------
SECRET_MESSAGE = bytes([13, 17])  # your example
N_TRIALS = 200
N_CHOICES = 10
A_TOTAL = 1.1
B_TOTAL = 1.3
SAFETY_BITS = 64  # extra precision cushion

# ----------------------------
# Precision helpers
# ----------------------------
def set_precision_for_bits(nbits: int, safety_bits: int = 32):
    """Size Decimal precision (in decimal digits) based on required binary precision."""
    prec_bits = nbits + safety_bits
    prec_digits = math.ceil(prec_bits * math.log10(2)) + 10
    decimal.getcontext().prec = prec_digits

# ----------------------------
# Build selections (your original style)
# ----------------------------
def build_selections(n_trials: int, n_choices: int, a_total: float, b_total: float, *, seed=None):
    if seed is not None:
        random.seed(seed)
    sels = []
    for _ in range(n_trials):
        vals = [random.random() for _ in range(n_choices)]
        vals = sorted(vals, reverse=True)
        choices = {i: v for i, v in enumerate(vals)}
        exps = [math.exp(v) for v in choices.values()]
        sum_exps = sum(exps)
        sum_exps *= random.uniform(a_total, b_total)  # intentional off-normalization
        sels.append({k: v / sum_exps for k, v in zip(choices.keys(), exps)})
    return sels

# ----------------------------
# Safer normalization (Decimal via str + exact closure)
# ----------------------------
def _norm_probs(dist):
    """
    Convert {idx: weight(float)} -> (keys, probs: Decimal[], cums: Decimal[])
    Normalizes to sum exactly 1 by forcing the last bin to close at 1.
    """
    keys = sorted(dist.keys())
    # Convert via str() to reduce float->Decimal noise
    ws = [Decimal(str(dist[k])) for k in keys]
    s = sum(ws)
    if s == 0:
        probs = [Decimal(1) / Decimal(len(keys)) for _ in keys]
    else:
        probs = [w / s for w in ws]

    cums = []
    acc = Decimal(0)
    for i, p in enumerate(probs):
        cums.append(acc)
        if i < len(probs) - 1:
            acc += p
        else:
            # Make the last probability exact so total == 1
            probs[i] = Decimal(1) - acc
            acc = Decimal(1)
    return keys, probs, cums  # cums[i] is the start of bin i

# ----------------------------
# Bit fraction <-> bytes
# ----------------------------
def _bytes_to_fraction(b: bytes):
    nbits = 8 * len(b)
    pow2 = 1 << nbits  # integer 2**nbits
    x = (Decimal(int.from_bytes(b, "big")) + Decimal("0.5")) / Decimal(pow2)
    return x, nbits

def _fraction_to_bytes(x: Decimal, nbits: int) -> bytes:
    pow2 = 1 << nbits
    one = Decimal(1)
    eps = one / Decimal(pow2)
    # Clamp numeric edges
    if x < 0:
        x = Decimal(0)
    if x >= 1:
        x = one - eps
    N = int((x * Decimal(pow2)).to_integral_value(rounding=ROUND_FLOOR))
    return N.to_bytes((nbits + 7) // 8, "big")

# ----------------------------
# Arithmetic-coding style encode/decode
# ----------------------------
def encode_indices(msg: bytes, selections):
    x, _nbits = _bytes_to_fraction(msg)  # x in [0,1)
    indices = []
    for dist in selections:
        keys, probs, cums = _norm_probs(dist)
        chosen = None
        for i, (lo, p) in enumerate(zip(cums, probs)):
            hi = lo + p
            # include right edge on last bin
            if (x >= lo and x < hi) or (i == len(probs) - 1 and x >= lo and x <= hi):
                chosen = i
                x = (x - lo) / p if p > 0 else Decimal(0)
                indices.append(keys[i])
                break
        if chosen is None:
            # extreme numeric edge: fall back to last bin
            i = len(probs) - 1
            indices.append(keys[i])
            x = Decimal(0)
    return indices

def decode_indices(indices, selections, out_nbytes):
    x = Decimal(0)
    for ind, dist in zip(indices, selections):
        keys, probs, cums = _norm_probs(dist)
        j = keys.index(ind)
        lo = cums[j]
        p = probs[j]
        x = lo + p * x
    return _fraction_to_bytes(x, 8 * out_nbytes)

# ----------------------------
# Capacity estimate (optional but helpful)
# ----------------------------
def estimate_capacity_bits(selections):
    """Rough Shannon capacity in bits across trials (float estimate is fine)."""
    total = 0.0
    for dist in selections:
        vals = list(dist.values())
        s = sum(vals) or 1.0
        ps = [v / s for v in vals if v > 0]
        H = -sum(p * math.log2(p) for p in ps)
        total += H
    return total

# ----------------------------
# Demo / main
# ----------------------------
if __name__ == "__main__":
    # 1) Build selections (keep them stable for encode & decode!)
    selections = build_selections(N_TRIALS, N_CHOICES, A_TOTAL, B_TOTAL, seed=12345)

    # 2) Precision sized to payload bits (+ cushion)
    msg_bits = 8 * len(SECRET_MESSAGE)
    set_precision_for_bits(msg_bits, safety_bits=SAFETY_BITS)

    # 3) Capacity check
    cap = estimate_capacity_bits(selections)
    print(f"Estimated capacity (bits): {cap:.2f}  |  Needed bits: {msg_bits}")
    if cap < msg_bits + 8:
        print("Warning: capacity is low. Consider more trials or flatter distributions.")

    # 4) Encode & decode
    indices = encode_indices(SECRET_MESSAGE, selections)
    recovered = decode_indices(indices, selections, out_nbytes=len(SECRET_MESSAGE))

    print("Encoded indices:", indices)
    print("Secret message:", list(SECRET_MESSAGE))
    print("Recovered     :", list(recovered))
    print("OK?", recovered == SECRET_MESSAGE)
