"""QIIME 2 plugin for samtools."""

import qiime2.plugin
from q2_types.sample_data import SampleData
from q2_types_genomics.per_sample_data._type import AlignmentMap
from qiime2.plugin import Bool, Int, Range, Str

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
    parameters={
        "threads": Int,
        "compression_level": Int % Range(0, 9, inclusive_end=True),  # type: ignore
        "memory_per_thread": Str,
        "name_sort": Bool,
        "tag": Str,
        "minimizer_sort": Bool,
        "kmer_size": Int,
    },
    outputs=[("output_bam", SampleData[AlignmentMap])],  # type: ignore
    input_descriptions={},
    parameter_descriptions={
        "threads": "-@ Set number of sorting and compression threads. By default, operation is single-threaded.",
        "compression_level": (
            "-l Set the desired compression level for the final output file, ranging from 0 "
            "(uncompressed) or 1 (fastest but minimal compression) to 9 (best compression but "
            "slowest to write), similarly to gzip(1)'s compression level setting."
        ),
        "memory_per_thread": (
            "-m Approximately the maximum required memory per thread, specified either in bytes "
            "or with a K, M, or G suffix. Default = 768 MiB, to prevent sort from creating a huge number of temporary"
            "files, it enforces a minimum value of 1M for this setting."
        ),
        "name_sort": ("-n Sort by read names (i.e., the QNAME field) rather than by chromosomal coordinates."),
        "tag": "-t TAG Sort first by the value in the alignment tag TAG, then by position or name (if also using name_sort)",
        "minimizer_sort": (
            "-M Sort unmapped reads (those in chromosome '*') by their sequence minimiser"
            "(Schleimer et al., 2003; Roberts et al., 2004), also reverse complementing as appropriate. "
            "This has the effect of collating some similar data together, improving the compressibility of the "
            "unmapped sequence. The minimiser kmer size is adjusted using the -K option. Note data compressed in "
            "this manner may need to be name collated prior to conversion back to fastq. Mapped sequences are sorted "
            "by chromosome and position."
        ),
        "kmer_size": "-K Sets the kmer size to be used in the mimizer_sort option. Default = 20",
    },
    output_descriptions={},
    name="samtools qiime plugin",
    description=(
        "Sort alignments by leftmost coordinates, by read name when -n is used, by tag contents with -t, or a minimiser-based collation order with -M. An appropriate @HD-SO sort order header tag will be added or an existing one updated if necessary. The sorted output is written to standard output by default, or to the specified file (out.bam) when -o is used. This command will also create temporary files tmpprefix.%d.bam as needed when the entire alignment data cannot fit into memory (as controlled via the -m option). Consider using samtools collate instead if you need name collated data without a full lexicographical sort. Note that if the sorted output file is to be indexed with samtools index, the default coordinate sort must be used. Thus the -n, -t and -M options are incompatible with samtools index. When sorting by minimisier (-M), the sort order is defined by the whole-read minimiser value and the offset into the read that this minimiser was observed. This produces small clusters (contig-like, but unaligned) and helps to improve compression with LZ algorithms. This can be improved by supplying a known reference to build a minimiser index (-I and -w options)."
    ),
)
