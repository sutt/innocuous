"""
LLM Steganography Package

A library for embedding and extracting hidden messages in LLM-generated text.
"""

from .core import main_encode, main_decode
from .llm import check_llm

__all__ = ["main_encode", "main_decode", "check_llm"]
__version__ = "0.1.0"
