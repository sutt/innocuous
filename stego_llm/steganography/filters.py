from typing import List, Tuple, Dict, Optional


def is_alpha_only(tok: str) -> bool:
    """Check if token contains only alphabetic characters and spaces."""
    return str(tok).replace(" ", "").isalpha()


def is_text_token(tok: str) -> bool:
    """Check if token is allowed for text generation (alpha + common punctuation)."""
    if tok.startswith("\\u"):
        return False
    if tok == "\n":
        return True
    if tok in [", ", ",", " ,", ".", ". "]:
        return True
    return str(tok).replace(" ", "").isalpha()


def find_acceptable_token(data: Dict) -> Optional[str]:
    """Return a token if it meets acceptance criteria; otherwise None."""
    pairs = [(k, v) for k, v in data.items()]
    if _acceptance_criteria_newline(pairs):
        return pairs[0][0]
    if _acceptance_criteria_threshold(pairs):
        return pairs[0][0]
    return None


def auto_accept_token(tok: str) -> bool:
    """
    Return true to decoder if this is a token auto-accepted via encoder
    e.g. common punctuation marks in v1 format.
    TODO - this should be refactored to handle variable enc/dec schemes.
    """
    return tok in [", ", ",", " ,", ".", ". ", "\n"]


def _acceptance_criteria_newline(pairs: List[Tuple[str, float]]) -> bool:
    """Accept if top token is a newline."""
    return pairs[0][0] == "\n"


def _acceptance_criteria_threshold(
    pairs: List[Tuple[str, float]], thresh: float = 0.7
) -> bool:
    """Accept if top token probability exceeds threshold."""
    return pairs[0][1] >= thresh


def pre_selection_filter(data: Dict) -> Dict:
    """Filter tokens before selection logic - allow common punctuation."""
    return {k: v for k, v in data.items() if is_text_token(k)}


def post_selection_filter(data: Dict) -> Dict:
    """Filter tokens after selection logic - disallow all punctuation."""
    return {k: v for k, v in data.items() if is_alpha_only(k)}
