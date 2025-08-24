"""
LLM Steganography Package

A library for embedding and extracting hidden messages in LLM-generated text.
"""

from .core import main_encode, main_decode

__all__ = ["main_encode", "main_decode"]
__version__ = "0.1.0"
