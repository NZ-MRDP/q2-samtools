"""QIIME 2 plugin for samtools."""

import qiime2.plugin
from q2_types.feature_data import FeatureData, Sequence
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
    inputs={"alignment_map": SampleData[AlignmentMap], "reference_fasta": FeatureData[Sequence]},  # type: ignore
    parameters={
        "threads": Int,
        "compression_level": Int % Range(0, 9, inclusive_end=True),  # type: ignore
        "memory_per_thread": Str,
        "name_sort": Bool,
        "tag_sort": Str,
        "minimizer_sort": Bool,
        "kmer_size": Int,
        "prefix": Str,
        "exclude_pg": Bool,
        "template_coordinate": Bool,
        "verbosity": Int,
    },
    outputs=[("output_bam", SampleData[AlignmentMap])],  # type: ignore
    input_descriptions={
        "alignment_map": "Input should be a bam file imported as a qza. A separate q2 plugin is planned to convert between bam, sam, and cram formats.",
        "reference_fasta": ("Reference DNA sequence FASTA"),
    },
    parameter_descriptions={
        "threads": "-@ Set number of sorting and compression threads. By default, operation is single-threaded.",
        "compression_level": (
            "Set the desired compression level for the final output file, ranging from 0 "
            "(uncompressed) or 1 (fastest but minimal compression) to 9 (best compression but "
            "slowest to write), similarly to gzip(1)'s compression level setting."
        ),
        "memory_per_thread": (
            "Approximately the maximum required memory per thread, specified either in bytes "
            "or with a K, M, or G suffix. Default = 768 MiB to prevent sort from creating a huge number of temporary"
            "files, it enforces a minimum value of 1M for this setting."
        ),
        "name_sort": ("Sort by read names (i.e., the QNAME field) rather than by chromosomal coordinates."),
        "tag_sort": "Sort first by the value in the alignment tag TAG, then by position or name (if also using name_sort)",
        "minimizer_sort": (
            "Sort unmapped reads (those in chromosome '*') by their sequence minimiser"
            "(Schleimer et al., 2003; Roberts et al., 2004), also reverse complementing as appropriate. "
            "This has the effect of collating some similar data together, improving the compressibility of the "
            "unmapped sequence. The minimiser kmer size is adjusted using the kmer_size option. Note: data compressed in "
            "this manner may need to be name collated prior to conversion back to fastq. Mapped sequences are sorted "
            "by chromosome and position."
        ),
        "kmer_size": "Sets the kmer size to be used in the mimizer_sort option. Default = 20",
        "prefix": (
            "Write temporary files to PREFIX.nnnn.bam, or if the specified PREFIX is an existing directory, "
            "to PREFIX/samtools.mmm.mmm.tmp.nnnn.bam, where mmm is unique to this invocation of the sort command. "
            "By default, any temporary files are written alongside the output file, as out.bam.tmp.nnnn.bam, "
            "or if output is to standard output, in the current directory as samtools.mmm.mmm.tmp.nnnn.bam."
        ),
        "template_coordinate": (
            "Sorts by template-coordinate, "
            "whereby the sort order (@HD SO) is unsorted, the group order (GO) is query, and the sub-sort (SS) is template-coordinate."
        ),
        "exclude_pg": "Do not add a @PG line to the header of the output file.",
        "verbosity": "Set level of verbosity",
    },
    output_descriptions={
        "output_bam": "Output is a bam file compressed in a qza. A separate q2 plugin is planned to convert between bam, sam, and cram formats."
    },
    name="samtools qiime plugin",
    description=(
        "Sort alignments by leftmost coordinates, by read name when name_sort is used, by tag contents with -t, "
        "or a minimiser-based collation order with minimizer_sort. An appropriate @HD-SO sort order header tag will be added "
        "or an existing one updated if necessary. The sorted output is written to standard output by default, "
        "or to the specified file (out.bam) when --o-output-bam or --output-dir are used. This command will also create temporary files"
        " 'tmpprefix.%d.bam' as needed when the entire alignment data cannot fit into memory (as controlled via the memory_per_thread"
        " option). Consider using samtools collate instead if you need name collated data without a full lexicographical sort. "
        "Note that if the sorted output file is to be indexed with samtools index, the default coordinate sort must be used. "
        "Thus the name_sort, tag_sort and minimizer_sort options are incompatible with samtools index. When sorting by minimisier "
        "(minimizer_sort), the sort order is defined by the whole-read minimiser value and the offset into the read that this minimiser "
        "was observed. This produces small clusters (contig-like, but unaligned) and helps to improve compression with LZ algorithms. "
        "This can be improved by supplying a known reference to build a minimiser index (reference_fasta option)."
    ),
)
