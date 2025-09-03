"""
LLM Steganography Package

A library for embedding and extracting hidden messages in LLM-generated text.
"""
from importlib import metadata

from .core import main_encode, main_decode
from .llm import check_llm

__all__ = ["main_encode", "main_decode", "check_llm", "__version__"]
try:
    __version__ = metadata.version("innocuous")
except metadata.PackageNotFoundError:
    __version__ = "0.0.0"  # Local development version
