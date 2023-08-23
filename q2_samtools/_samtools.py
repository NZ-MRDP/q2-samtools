import os
import subprocess

from q2_types_genomics.per_sample_data._format import BAMDirFmt, BAMFormat


# TODO: Add in arguments/flags
# TODO: Make sure .sam/.cram files work - low priority
# TODO: maybe add another method that allows transformations from .sam/.cram to .bam
def sort(alignment_map: BAMDirFmt) -> BAMDirFmt:
    """sort."""
    output_bam = BAMDirFmt()
    for path, _ in alignment_map.bams.iter_views(view_type=BAMFormat):  # type: ignore
        cmd = [
            "samtools",
            "sort",
            os.path.join(str(alignment_map.path), str(path.stem) + ".bam"),
            "-o",
            os.path.join(str(output_bam), str(path.stem) + ".bam"),
        ]
        subprocess.run(cmd, check=True)
    return output_bam


# TODO: Get this plugin working
def faidx():
    """faidx."""
    pass
