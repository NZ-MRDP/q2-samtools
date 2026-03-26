"""samtools actions used by the QIIME 2 plugin."""

import os
import subprocess
from typing import Optional, Union

from q2_types.feature_data import DNAFASTAFormat, RNAFASTAFormat
from q2_types.per_sample_sequences import BAMDirFmt, BAMFormat
from q2_types_variant import (
    SamtoolsIndexSequencesDirectoryFormat,
    SamtoolsRegionFileFormat,
)
from qiime2.util import duplicate

# TODO: Make sure .sam/.cram files work - low priority
# TODO: maybe add another method that allows transformations from .sam/.cram to .bam


def sort(
    alignment_map: BAMDirFmt,
    reference_sequences: Optional[Union[DNAFASTAFormat, RNAFASTAFormat]] = None,
    threads: int = 1,
    compression_level: int = 1,
    memory_per_thread: str = "768M",
    name_sort: bool = False,
    lexicographical_name_sort: bool = False,
    tag_sort: Optional[str] = None,
    minimizer_sort: bool = False,
    kmer_size: int = 20,
    minimizer_window: Optional[int] = None,
    minimizer_reference_index: Optional[str] = None,
    homopolymer_squash: bool = False,
    prefix: Optional[str] = None,
    template_coordinate: bool = False,
    exclude_pg: bool = False,
    verbosity: int = 1,
) -> BAMDirFmt:
    """Sort BAM files with samtools."""
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
        if lexicographical_name_sort:
            cmd.append("-N")
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
        if minimizer_window is not None:
            cmd.extend(["-w", str(minimizer_window)])
        if minimizer_reference_index:
            cmd.extend(["-I", minimizer_reference_index])
        if homopolymer_squash:
            cmd.append("-H")
        if reference_sequences:
            cmd.extend(["--reference", str(reference_sequences)])
        subprocess.run(cmd, check=True)
    return output_bam


def extract_fasta_subsequence(
    reference_sequences: DNAFASTAFormat,
    region_file: SamtoolsRegionFileFormat,
    input_fai: SamtoolsIndexSequencesDirectoryFormat,
    ignore_missing_region: bool = False,
    fasta_length: int = 60,
    reverse_complement: bool = False,
    mark_strand: str = "rc",
) -> DNAFASTAFormat:
    """Extract subsequences from an indexed FASTA file."""
    fasta_subsequence = DNAFASTAFormat()
    cmd = [
        "samtools",
        "faidx",
        str(reference_sequences),
        "--region-file",
        str(region_file),
        "--fai-idx",
        input_fai.reference_fasta_index_filepath,
        "-n",
        str(fasta_length),
        "-o",
        str(fasta_subsequence),
        "--mark-strand",
        str(mark_strand),
    ]
    if ignore_missing_region:
        cmd.append("-c")
    if reverse_complement:
        cmd.append("-i")
    subprocess.run(cmd, check=True)
    return fasta_subsequence


def index_sequences(
    reference_sequences: DNAFASTAFormat,
) -> SamtoolsIndexSequencesDirectoryFormat:
    """Create samtools and GATK index files for a reference FASTA."""
    output_fai = SamtoolsIndexSequencesDirectoryFormat()

    cmd_samtools = [
        "samtools",
        "faidx",
        str(reference_sequences),
        "-o",
        os.path.join(str(output_fai), "dna-sequences.fasta.fai"),
    ]
    subprocess.run(cmd_samtools, check=True)

    duplicate(str(reference_sequences), os.path.join(str(output_fai), "dna-sequences.fasta"))

    cmd_gatk = [
        "gatk",
        "CreateSequenceDictionary",
        "-R",
        output_fai.reference_fasta_filepath,
        "-O",
        os.path.join(str(output_fai), "dna-sequences.dict"),
    ]
    subprocess.run(cmd_gatk, check=True)

    return output_fai
