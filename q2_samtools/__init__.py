"""samtools python library."""
from ._samtools import align_paired, align_single, build

__version__ = "0.0.0"

__all__ = ["build", "align_single", "align_paired"]
