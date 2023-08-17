import os
import subprocess
import tempfile

import pandas as pd
from q2_types.samtools2 import samtools2IndexDirFmt
from q2_types.feature_data import DNAFASTAFormat
from q2_types.per_sample_sequences import (
    CasavaOneEightSingleLanePerSampleDirFmt,
    SingleLanePerSamplePairedEndFastqDirFmt,
    SingleLanePerSampleSingleEndFastqDirFmt,
)
from q2_types_genomics.per_sample_data import BAMDirFmt


def build(reference_seqs: DNAFASTAFormat) -> samtools2IndexDirFmt:
    """build."""
    samtools_database = samtools2IndexDirFmt()

    cmd = [
        "samtools2-build",
        str(reference_seqs),
        os.path.join(str(samtools_database), "samtools2_index"),
    ]
    subprocess.run(cmd, check=True)
    return samtools_database


# TODO: Refactor redundant code throughout
def align_paired(
    samtools_database: samtools2IndexDirFmt,
    demultiplexed_sequences: SingleLanePerSamplePairedEndFastqDirFmt,
    threads: int = 1,
) -> (CasavaOneEightSingleLanePerSampleDirFmt, CasavaOneEightSingleLanePerSampleDirFmt, BAMDirFmt,):  # type: ignore
    """align_paired.

    Parameters
    ----------
    samtools_database : samtools2IndexDirFmt
        samtools_database
    demultiplexed_sequences : SingleLanePerSampleSingleEndFastqDirFmt
        demultiplexed_sequences
    threads : int, optional
        number of alignment threads to launch. Defaults to 1.

    Returns
    -------
    (CasavaOneEightSingleLanePerSampleDirFmt, CasavaOneEightSingleLanePerSampleDirFmt)

    """
    """align."""
    aligned_filtered_seqs = CasavaOneEightSingleLanePerSampleDirFmt()
    unaligned_filtered_seqs = CasavaOneEightSingleLanePerSampleDirFmt()
    samtools_alignment = BAMDirFmt()
    df = demultiplexed_sequences.manifest.view(pd.DataFrame)
    for sample_id, fwd, rev in df.itertuples():
        # samtools renames fwd and rev sequences with .1 and 2.
        # so we give them a temporary name and change it back to what it should be later
        aligned_path = os.path.join(str(aligned_filtered_seqs), "temp_name")
        unaligned_path = os.path.join(str(unaligned_filtered_seqs), "temp_name")
        cmd = [
            "samtools2",
            "-x",
            os.path.join(str(samtools_database), "samtools2_index"),
            "-1",
            str(fwd),
            "-2",
            str(rev),
            "--un-conc-gz",
            aligned_path,
            "--al-conc-gz",
            unaligned_path,
            "--threads",
            str(threads),
        ]

        with tempfile.NamedTemporaryFile() as temp:
            subprocess.run(cmd, check=True, stdout=temp)
            with open(os.path.join(str(samtools_alignment), f"{sample_id}.bam"), "w") as samtools_file:
                subprocess.run(["samtools", "view", "-bS", temp.name], check=True, stdout=samtools_file)

        # rename the files what they should be
        os.rename(aligned_path + ".1", os.path.join(str(aligned_filtered_seqs), os.path.basename(fwd)))
        os.rename(aligned_path + ".2", os.path.join(str(aligned_filtered_seqs), os.path.basename(rev)))
        os.rename(unaligned_path + ".1", os.path.join(str(unaligned_filtered_seqs), os.path.basename(fwd)))
        os.rename(unaligned_path + ".2", os.path.join(str(unaligned_filtered_seqs), os.path.basename(rev)))
    return aligned_filtered_seqs, unaligned_filtered_seqs, samtools_alignment


def align_single(
    samtools_database: samtools2IndexDirFmt,
    demultiplexed_sequences: SingleLanePerSampleSingleEndFastqDirFmt,
    threads: int = 1,
) -> (CasavaOneEightSingleLanePerSampleDirFmt, CasavaOneEightSingleLanePerSampleDirFmt, BAMDirFmt):  # type: ignore
    """align_single.

    Parameters
    ----------
    samtools_database : samtools2IndexDirFmt
        samtools_database
    demultiplexed_sequences : SingleLanePerSampleSingleEndFastqDirFmt
        demultiplexed_sequences
    threads : int, optional
        number of alignment threads to launch. Defaults to 1.

    Returns
    -------
    (CasavaOneEightSingleLanePerSampleDirFmt, CasavaOneEightSingleLanePerSampleDirFmt)

    """
    aligned_filtered_seqs = CasavaOneEightSingleLanePerSampleDirFmt()
    unaligned_filtered_seqs = CasavaOneEightSingleLanePerSampleDirFmt()
    samtools_alignment = BAMDirFmt()
    df = demultiplexed_sequences.manifest.view(pd.DataFrame)
    for sample_id, sample_path in df.itertuples():
        cmd = [
            "samtools2",
            "-x",
            os.path.join(str(samtools_database), "samtools2_index"),
            "-U",
            str(sample_path),
            "--un-gz",
            os.path.join(str(unaligned_filtered_seqs), os.path.basename(sample_path)),
            "--al-gz",
            os.path.join(str(aligned_filtered_seqs), os.path.basename(sample_path)),
            "--threads",
            str(threads),
        ]
        with tempfile.NamedTemporaryFile() as temp:
            subprocess.run(cmd, check=True, stdout=temp)
            with open(os.path.join(str(samtools_alignment), f"{sample_id}.bam"), "w") as samtools_file:
                subprocess.run(["samtools", "view", "-bS", temp.name], check=True, stdout=samtools_file)

    return aligned_filtered_seqs, unaligned_filtered_seqs, samtools_alignment
