"""
SAIA - Models' Information Module.

Version: 2024.08.02.01
"""

from enum import StrEnum


class EOM(StrEnum):
    """Enum of Ollama Local Model Names."""

    # Meta
    L008 = "llama3.1"  # 8k = 5.3GB, 128k = 56GB
    L070 = "llama3.1:70b"  # 8k = 47 GB

    # Microsoft
    P003 = "phi3:mini-128k"
    P014 = "phi3:medium-128k"  # context window 128k

    # Mistral and Nvidia
    M012 = "mistral-nemo"  # 8k = 7.8GB, 128k = 69GB
    M123 = "mistral-large:123b-instruct-2407-q2_K"

    # Google
    G009 = "gemma2"  # context window 8k
    G027 = "gemma2:27b"  # context window 8k


class Info:
    """Info Class."""

    Assistant_List: list[list[str]] = [
        ["小娜", "L008", EOM.L008],  # Llama
        ["小季", "G009", EOM.G009],  # Gemma
        ["小菲", "P003", EOM.P003],  # Phi
        ["小米", "M012", EOM.M012],  # Mistral
        ["娜姐", "L070", EOM.L070],  # Llama
        ["季哥", "G027", EOM.G027],  # Gemma
        ["菲姐", "P014", EOM.P014],  # Phi
        ["米哥", "M123", EOM.M123],  # Mistral
    ]
