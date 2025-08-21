from typing import (
    List,
    Tuple,
)

def filter_non_alpha(data: dict) -> dict:
    return {
        k:v for k,v in data.items()
        if str(k).replace(" ", "").isalpha()
    }

def filter_tok(data: dict) -> dict:
    return {
        k:v for k,v in data.items()
        if allowed_2(k)
    }

def allowed_1(tok: str):
    """allowed: only isalpha and spaces"""
    return str(tok).replace(" ", "").isalpha()

def allowed_2(tok: str):
    """allowed: only isalpha and spaces"""
    if tok.startswith("\\u"): return False
    if tok == "\n": return True
    if tok == ", ": return True
    if tok == ",": return True
    if tok == " ,": return True
    if tok == ".": return True
    if tok == ". ": return True
    return str(tok).replace(" ", "").isalpha()

def accept_tok(data: dict) -> str | None:
    """return a token if acceptance is a match; otherwise None"""
    pairs = [(k,v) for k,v in data.items()]    
    if acceptance_criteria_1(pairs): return pairs[0][0]
    if acceptance_criteria_2(pairs): return pairs[0][0]
    return None

def acceptance_criteria_1(pairs: List[Tuple[str, float]]) -> bool:
    if pairs[0][0] == "\n": return True
    return False

def acceptance_criteria_2(pairs: List[Tuple[str, float]], thresh=0.7) -> bool:
    if pairs[0][1] >= thresh: return True
    return False
    



if __name__ == "__main__":
    assert len(filter_non_alpha({"abc":1})) == 1
    assert len(filter_non_alpha({" a ":1})) == 1
    assert len(filter_non_alpha({"a'":1})) == 0
    assert len(filter_non_alpha({"!":1})) == 0