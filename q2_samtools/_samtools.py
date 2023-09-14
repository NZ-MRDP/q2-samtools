import os
import subprocess
from typing import Union

from q2_types.feature_data._format import (
    DNAFASTAFormat,
    DNASequencesDirectoryFormat,
    RNAFASTAFormat,
)
from q2_types.metadata import ImmutableMetadataFormat
from q2_types_genomics.per_sample_data._format import BAMDirFmt, BAMFormat

from ._format import SamtoolsIndexFileFormat

# TODO: Add in arguments/flags
# TODO: Make sure .sam/.cram files work - low priority
# TODO: maybe add another method that allows transformations from .sam/.cram to .bam


def sort(
    alignment_map: BAMDirFmt,
    reference_fasta: Union[DNAFASTAFormat, RNAFASTAFormat] = None,
    threads: int = 1,
    compression_level: int = 1,
    memory_per_thread: str = "768M",
    name_sort: bool = False,
    tag_sort: str = None,
    minimizer_sort: bool = False,
    kmer_size: int = 20,
    prefix: str = None,
    template_coordinate: bool = False,
    exclude_pg: bool = False,
    verbosity: int = 1,
) -> BAMDirFmt:
    """sort."""
    output_bam = BAMDirFmt()
    for path, _ in alignment_map.bams.iter_views(view_type=BAMFormat):  # type: ignore
        cmd = [
            "samtools",
            "sort",
            os.path.join(str(alignment_map.path), str(path.stem) + ".bam"),
            "-@",
            str(threads),
            "-l",
            str(compression_level),
            "-m",
            str(memory_per_thread),
            "-o",
            os.path.join(str(output_bam), str(path.stem) + ".bam"),
            "--verbosity",
            str(verbosity),
        ]
        if name_sort:
            cmd.append("-n")
        if exclude_pg:
            cmd.append("--no-PG")
        if template_coordinate:
            cmd.append("--template-coordinate")
        if prefix:
            cmd.extend(["-T", str(prefix)])
        if tag_sort:
            cmd.extend(["-t", str(tag_sort)])
        if minimizer_sort:
            cmd.extend(["-M", "-K", str(kmer_size)])
        if reference_fasta:
            cmd.extend(["--reference", str(reference_fasta)])
        subprocess.run(cmd, check=True)
    return output_bam


# TODO: Get this plugin working. What is the correct type/format for the output_fai?
def faidx(
    reference_fasta: DNAFASTAFormat,
) -> SamtoolsIndexFileFormat:
    """faidx."""
    output_fai = SamtoolsIndexFileFormat()
    cmd = [
        "samtools",
        "faidx",
        str(reference_fasta),
        "-o",
        str(output_fai),
    ]
    subprocess.run(cmd, check=True)
    return output_fai
