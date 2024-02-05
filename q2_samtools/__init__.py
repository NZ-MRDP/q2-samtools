"""samtools python library."""
from ._samtools import extract_fasta_subsequence, index_sequences, sort

__version__ = "0.1.4"

__all__ = ["sort", "index_sequences", "extract_fasta_subsequence"]
