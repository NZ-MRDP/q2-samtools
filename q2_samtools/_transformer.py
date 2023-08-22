from typing import List

from q2_types_genomics.per_sample_data._format import BAMDirFmt, BAMFormat


@plugin.register_transformer
def _1(data: BAMDirFmt) -> List[BAMFormat]:
    list_bam_fmt = list()
    for output in data:
        filename = f"{output.sample_id}_{output.type}_keystones.json"
        with open(dirfmt.path / filename, "w") as fh:
            json.dump(output.dict(), fh)

    return dirfmt
