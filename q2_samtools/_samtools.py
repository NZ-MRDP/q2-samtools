import os
import shutil
import subprocess
from typing import Union

from q2_types.feature_data._format import DNAFASTAFormat, RNAFASTAFormat
from q2_types_genomics.per_sample_data._format import BAMDirFmt, BAMFormat

from ._format import (DictDirFormat, DictFileFormat, SamtoolsIndexFileFormat,
                      SamtoolsIndexSequencesDirectoryFormat,
                      SamtoolsRegionFileFormat)

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


def extract_fasta_subsequence(
    reference_fasta: DNAFASTAFormat,
    region_file: SamtoolsRegionFileFormat,
    input_fai: SamtoolsIndexFileFormat,
    ignore_missing_region: bool = False,
    fasta_length: int = 60,
    reverse_complement: bool = False,
    mark_strand: str = "rc",
) -> DNAFASTAFormat:
    """extract_fasta_subsequence."""
    fasta_subsequence = DNAFASTAFormat()
    cmd = [
        "samtools",
        "faidx",
        str(reference_fasta),
        "--region-file",
        str(region_file),
        "--fai-idx",
        str(input_fai),
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


def index_fasta(
    reference_fasta: DNAFASTAFormat,
) -> (SamtoolsIndexSequencesDirectoryFormat, SamtoolsIndexSequencesDirectoryFormat):
    """index_fasta."""
    output_fai = SamtoolsIndexSequencesDirectoryFormat()
    dict = SamtoolsIndexSequencesDirectoryFormat()
    cmd = [
        "samtools",
        "faidx",
        str(reference_fasta),
        "-o",
        os.path.join(str(output_fai), 
                     os.path.basename(str(reference_fasta) + ".fai")),
    ]
    subprocess.run(cmd, check=True)
    cmd = [
        "gatk",
        "CreateSequenceDictionary",
        "-R",
        str(reference_fasta),
        "-O",
        os.path.join(str(dict), "dna-sequences.dict"),
    ]
    subprocess.run(cmd, check=True)
    shutil.copyfile(str(reference_fasta), 
                    os.path.join(str(output_fai), 
                                 os.path.basename(str(reference_fasta))))
    shutil.copyfile(os.path.join(str(dict), "dna-sequences.dict"), 
                    os.path.join(str(output_fai), 
                                 os.path.basename(str(reference_fasta))))
    return output_fai, dict
