"""QIIME 2 plugin for samtools."""

import qiime2.plugin
from q2_types.sample_data import SampleData
from q2_types_genomics.per_sample_data._type import AlignmentMap
from qiime2.plugin import Int

import q2_samtools

plugin = qiime2.plugin.Plugin(
    name="samtools",
    version="0.0.0",
    description="QIIME 2 plugin for samtools",
    website="http://www.htslib.org/",
    package="q2_samtools",
    user_support_text=("I'm sorry you're having problems"),
    citation_text=("https://pubmed.ncbi.nlm.nih.gov/33590861/"),
)

plugin.methods.register_function(
    function=q2_samtools.sort,
    inputs={"alignment_map": SampleData[AlignmentMap]},  # type: ignore
    parameters={"threads": Int},
    outputs=[("output_bam", SampleData[AlignmentMap])],  # type: ignore
    input_descriptions={},
    parameter_descriptions={
        "threads": "INT Set number of sorting and compression threads. By default, operation is single-threaded."
    },
    output_descriptions={},
    name="samtools qiime plugin",
    description=(
        "Sort alignments by leftmost coordinates, by read name when -n is used, by tag contents with -t, or a minimiser-based collation order with -M. An appropriate @HD-SO sort order header tag will be added or an existing one updated if necessary. The sorted output is written to standard output by default, or to the specified file (out.bam) when -o is used. This command will also create temporary files tmpprefix.%d.bam as needed when the entire alignment data cannot fit into memory (as controlled via the -m option). Consider using samtools collate instead if you need name collated data without a full lexicographical sort. Note that if the sorted output file is to be indexed with samtools index, the default coordinate sort must be used. Thus the -n, -t and -M options are incompatible with samtools index. When sorting by minimisier (-M), the sort order is defined by the whole-read minimiser value and the offset into the read that this minimiser was observed. This produces small clusters (contig-like, but unaligned) and helps to improve compression with LZ algorithms. This can be improved by supplying a known reference to build a minimiser index (-I and -w options)."
    ),
)
