# bitcoin_addr_codec.py
# Python 3.8+

from typing import Tuple, Dict, Any, Optional

# ---------------- Base58 / Base58Check ----------------

_B58_ALPHABET = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
_B58_IDX = {c: i for i, c in enumerate(_B58_ALPHABET)}


def b58encode(b: bytes) -> str:
    # Count leading zeros
    n_zeros = len(b) - len(b.lstrip(b"\0"))
    num = int.from_bytes(b, "big")
    out = ""
    while num:
        num, rem = divmod(num, 58)
        out = _B58_ALPHABET[rem] + out
    return "1" * n_zeros + out


def b58decode(s: str) -> bytes:
    if not s:
        return b""
    num = 0
    for c in s:
        if c not in _B58_IDX:
            raise ValueError("Invalid Base58 character")
        num = num * 58 + _B58_IDX[c]
    # Convert to bytes
    full = num.to_bytes((num.bit_length() + 7) // 8, "big") or b"\0"
    # Restore leading zeros
    n_zeros = len(s) - len(s.lstrip("1"))
    return b"\0" * n_zeros + full


def _double_sha256(b: bytes) -> bytes:
    import hashlib

    return hashlib.sha256(hashlib.sha256(b).digest()).digest()


def base58check_encode(version: bytes, payload: bytes) -> str:
    body = version + payload
    checksum = _double_sha256(body)[:4]
    return b58encode(body + checksum)


def base58check_decode(s: str) -> Tuple[bytes, bytes]:
    raw = b58decode(s)
    if len(raw) < 5:
        raise ValueError("Base58Check: too short")
    body, checksum = raw[:-4], raw[-4:]
    if _double_sha256(body)[:4] != checksum:
        raise ValueError("Base58Check: bad checksum")
    return body[:1], body[1:]  # (version_byte, payload)


# ---------------- Bech32 / Bech32m (BIP-173, BIP-350) ----------------

_BECH32_CHARSET = "qpzry9x8gf2tvdw0s3jn54khce6mua7l"
_BECH32_MAP = {c: i for i, c in enumerate(_BECH32_CHARSET)}


def _bech32_hrp_expand(hrp: str):
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def _bech32_polymod(values) -> int:
    GEN = [0x3B6A57B2, 0x26508E6D, 0x1EA119FA, 0x3D4233DD, 0x2A1462B3]
    chk = 1
    for v in values:
        b = chk >> 25
        chk = ((chk & 0x1FFFFFF) << 5) ^ v
        for i in range(5):
            chk ^= GEN[i] if ((b >> i) & 1) else 0
    return chk


# Constants: BIP-173 (bech32) and BIP-350 (bech32m)
_CONST_BECH32 = 1
_CONST_BECH32M = 0x2BC830A3


def _bech32_verify_checksum(hrp: str, data) -> str:
    pm = _bech32_polymod(_bech32_hrp_expand(hrp) + data)
    if pm == _CONST_BECH32:
        return "bech32"
    if pm == _CONST_BECH32M:
        return "bech32m"
    raise ValueError("Bech32: bad checksum")


def _bech32_create_checksum(hrp: str, data, spec: str):
    const = _CONST_BECH32 if spec == "bech32" else _CONST_BECH32M
    pm = _bech32_polymod(_bech32_hrp_expand(hrp) + data + [0] * 6) ^ const
    return [(pm >> 5 * (5 - i)) & 31 for i in range(6)]


def bech32_decode(addr: str) -> Tuple[str, list, str]:
    if any(ord(x) < 33 or ord(x) > 126 for x in addr):
        raise ValueError("Bech32: invalid chars")
    if addr.lower() != addr and addr.upper() != addr:
        raise ValueError("Bech32: mixed case")
    addr = addr.lower()
    if (
        ("1" not in addr)
        or (addr.rfind("1") == 0)
        or (addr.rfind("1") == len(addr) - 1)
    ):
        raise ValueError("Bech32: invalid separator position")
    pos = addr.rfind("1")
    hrp = addr[:pos]
    data_part = addr[pos + 1 :]
    data = []
    for c in data_part:
        if c not in _BECH32_MAP:
            raise ValueError("Bech32: invalid data char")
        data.append(_BECH32_MAP[c])
    if len(data) < 6:
        raise ValueError("Bech32: too short data")
    spec = _bech32_verify_checksum(hrp, data)
    return hrp, data[:-6], spec


def bech32_encode(hrp: str, data: list, spec: str) -> str:
    if spec not in ("bech32", "bech32m"):
        raise ValueError("spec must be 'bech32' or 'bech32m'")
    combined = data + _bech32_create_checksum(hrp, data, spec)
    return hrp + "1" + "".join(_BECH32_CHARSET[d] for d in combined)


def convertbits(data: bytes, from_bits: int, to_bits: int, pad: bool) -> Optional[list]:
    # General power-of-2 base conversion (e.g., 8->5 or 5->8)
    acc = 0
    bits = 0
    ret = []
    maxv = (1 << to_bits) - 1
    for b in data:
        if b < 0 or (b >> from_bits):
            return None
        acc = (acc << from_bits) | b
        bits += from_bits
        while bits >= to_bits:
            bits -= to_bits
            ret.append((acc >> bits) & maxv)
    if pad:
        if bits:
            ret.append((acc << (to_bits - bits)) & maxv)
    elif bits >= from_bits or ((acc << (to_bits - bits)) & maxv):
        return None
    return ret


# ---------------- High-level address encode/decode ----------------

# Known version bytes (Base58Check)
_VERSION_MAP = {
    0x00: ("mainnet", "p2pkh"),
    0x05: ("mainnet", "p2sh"),
    0x6F: ("testnet", "p2pkh"),
    0xC4: ("testnet", "p2sh"),
}


def _infer_segwit_type(wver: int, program: bytes) -> str:
    if wver == 0:
        if len(program) == 20:
            return "p2wpkh"
        if len(program) == 32:
            return "p2wsh"
        return "witness_v0"
    if wver == 1 and len(program) == 32:
        return "p2tr"  # Taproot
    return f"witness_v{wver}"


def decode_bitcoin_address(addr: str) -> Dict[str, Any]:
    """
    Returns a dict describing the address and its underlying bytes.

    For Base58:
      {format, network, type, version_byte, payload (hash160)}

    For Bech32/Bech32m:
      {format, network(hrp), spec, witness_version, program}
    """
    # Try Base58Check first
    try:
        v, payload = base58check_decode(addr)
        v_int = v[0]
        network, a_type = _VERSION_MAP.get(v_int, ("unknown", "unknown"))
        return {
            "format": "base58",
            "network": network,
            "type": a_type,
            "version_byte": v_int,
            "payload": payload,  # typically 20 bytes (hash160)
            "payload_hex": payload.hex(),
        }
    except Exception:
        pass

    # Try Bech32 / Bech32m
    hrp, data, spec = bech32_decode(addr)
    if len(data) < 1:
        raise ValueError("SegWit: missing witness version")
    wver = data[0]
    prog5 = data[1:]
    if wver < 0 or wver > 16:
        raise ValueError("SegWit: invalid witness version")
    program = bytes(convertbits(bytes(prog5), 5, 8, False) or b"")
    # Per BIP-173/350 basic size checks
    if len(program) < 2 or len(program) > 40:
        raise ValueError("SegWit: invalid program length")

    # Validate checksum rule against version (BIP-350)
    if wver == 0 and spec != "bech32":
        raise ValueError("SegWit v0 must use bech32 checksum")
    if wver != 0 and spec != "bech32m":
        raise ValueError("SegWit v1+ must use bech32m checksum")

    return {
        "format": "bech32",
        "network": hrp,
        "spec": spec,
        "witness_version": wver,
        "program": program,
        "program_hex": program.hex(),
        "type": _infer_segwit_type(wver, program),
    }


def encode_base58_address(version_byte: int, payload: bytes) -> str:
    """
    Encode (version_byte + payload) with Base58Check.
    payload is typically a 20-byte hash160 for P2PKH/P2SH.
    """
    if not (0 <= version_byte <= 255):
        raise ValueError("version_byte must be 0..255")
    return base58check_encode(bytes([version_byte]), payload)


def encode_segwit_address(hrp: str, witness_version: int, program: bytes) -> str:
    """
    Encode a SegWit address per BIP-173/350.
    hrp: 'bc' (mainnet), 'tb' (testnet), 'bcrt' (regtest)
    witness_version: 0..16
    program: 2..40 bytes
    """
    if not (0 <= witness_version <= 16):
        raise ValueError("witness_version must be 0..16")
    if not (2 <= len(program) <= 40):
        raise ValueError("program length must be 2..40 bytes")
    spec = "bech32" if witness_version == 0 else "bech32m"
    data = [witness_version] + (convertbits(program, 8, 5, True) or [])
    return bech32_encode(hrp, data, spec)


# ---------------- Convenience helpers ----------------


def describe(addr: str) -> str:
    """Pretty string description."""
    info = decode_bitcoin_address(addr)
    if info["format"] == "base58":
        return (
            f"{addr}\n"
            f"  Format: Base58Check ({info['type']}, {info['network']})\n"
            f"  Version: 0x{info['version_byte']:02x}\n"
            f"  Payload ({len(info['payload'])} bytes): {info['payload_hex']}"
        )
    else:
        return (
            f"{addr}\n"
            f"  Format: Bech32 ({info['spec']})\n"
            f"  Network HRP: {info['network']}\n"
            f"  Witness v{info['witness_version']} ({info['type']})\n"
            f"  Program ({len(info['program'])} bytes): {info['program_hex']}"
        )


if __name__ == "__main__":
    # print(describe("1BoatSLRHtKNngkdXEeobR76b53LETtpyT"))      # P2PKH mainnet
    # bc1pt65exley6pv6uqws7xr3ku7u922tween0nfyz257rnl5300cjnrsjp9er6
    print(describe("12Wfw4L3oPJFk2q6osDoZLYAwdFkhvgt4E"))
