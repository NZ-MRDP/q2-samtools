import os
import subprocess

from q2_types_genomics.per_sample_data._format import BAMDirFmt, BAMFormat


# TODO: Add in arguments/flags
# TODO: Make sure .sam/.cram files work - low priority
# TODO: maybe add another method that allows transformations from .sam/.cram to .bam
#
def sort(
    alignment_map: BAMDirFmt,
    threads: int = 1,
    compression_level: int = 1,
    memory_per_thread: str = "768M",
    name_sort: bool = False,
    tag_sort: str = "",
    minimizer_sort: bool = False,
    kmer_size: int = 20,
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
        ]
        if name_sort:
            cmd.append("-n")
        if tag:
            cmd.extend(["-t", tag_sort])
        if minimizer_sort:
            cmd.extend(["-M", "-K", str(kmer_size)])
        subprocess.run(cmd, check=True)
    return output_bam


# TODO: Get this plugin working
def faidx():
    """faidx."""
    pass
