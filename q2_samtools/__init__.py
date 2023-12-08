"""samtools python library."""
from ._samtools import extract_fasta_subsequence, index_fasta, sort
from ._type import DictType, SamtoolsIndexFormat, SamtoolsRegionFormat

__version__ = "0.0.0"

__all__ = ["sort", "index_fasta", "extract_fasta_subsequence", "SamtoolsIndexFormat", "SamtoolsRegionFormat", "DictType"]
