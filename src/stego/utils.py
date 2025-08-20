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
    if "\\n" in tok: return True
    if "," in tok: return True
    if "." in tok: return True
    return str(tok).replace(" ", "").isalpha()

if __name__ == "__main__":
    assert len(filter_non_alpha({"abc":1})) == 1
    assert len(filter_non_alpha({" a ":1})) == 1
    assert len(filter_non_alpha({"a'":1})) == 0
    assert len(filter_non_alpha({"!":1})) == 0