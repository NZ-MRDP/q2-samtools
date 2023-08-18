import os
import subprocess
import tempfile

import pandas as pd
from q2_types.sample_data import SampleData
from q2_types_genomics.per_sample_data._type import AlignmentMap


def sort(alignment_map: SampleData[AlignmentMap]) -> SampleData[AlignmentMap]:
    """sort."""

    cmd = [
        "samtools sort",
        str(alignment_map),
    ]
    subprocess.run(cmd, check=True)
    return sorted_alignment_map
