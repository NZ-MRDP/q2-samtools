import os
import subprocess
import tempfile

import pandas as pd
from q2_types.sample_data import SampleData
from q2_types_genomics.per_sample_data._format import BAMDirFmt
from q2_types_genomics.per_sample_data._type import AlignmentMap


def sort(alignment_map: BAMDirFmt) -> BAMDirFmt:
    """sort."""
    output_bam = BAMDirFmt()
    for b in alignment_map:
        cmd = ["samtools", "sort", str(alignment_map), "-o", str(output_bam)]
        subprocess.run(cmd, check=True)
    return output_bam
