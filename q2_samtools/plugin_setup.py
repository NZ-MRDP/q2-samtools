"""QIIME 2 plugin for samtools."""

import q2_samtools
import qiime2.plugin
from q2_types.feature_data import FeatureData, Sequence
from q2_types.sample_data import SampleData
from q2_types_genomics.per_sample_data._type import AlignmentMap
from qiime2.plugin import Bool, Int, Range, Str

from ._format import (DictDirFormat, DictFileFormat, SamtoolsIndexDirFormat,
                      SamtoolsIndexSequencesDirectoryFormat,
                      SamtoolsRegionDirFormat)
from ._type import (DictType, SamtoolsIndexFormat,
                    SamtoolsIndexSequencesFormat, SamtoolsRegionFormat)

plugin = qiime2.plugin.Plugin(
    name="samtools",
    version="0.0.0",
    description="QIIME 2 plugin for samtools",
    website="http://www.htslib.org/",
    package="q2_samtools",
    user_support_text=("I'm sorry you're having problems"),
    citation_text=("https://pubmed.ncbi.nlm.nih.gov/33590861/"),
)

plugin.methods.register_function(function=q2_samtools.sort,
    inputs={"alignment_map": SampleData[AlignmentMap], "reference_fasta": FeatureData[Sequence]},
    parameters={
        "threads": Int,
        "compression_level": Int % Range(0, 9, inclusive_end=True),
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
    outputs=[("output_bam", SampleData[AlignmentMap])],
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
    name="sort bam files",
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

plugin.methods.register_function(function=q2_samtools.extract_fasta_subsequence,
    inputs={
        "reference_fasta": FeatureData[Sequence],
        "region_file": FeatureData[SamtoolsRegionFormat],
        "input_fai": FeatureData[SamtoolsIndexFormat],
    },
    parameters={
        "ignore_missing_region": Bool,
        "reverse_complement": Bool,
        "fasta_length": Int,
        "mark_strand": Str,
    },
    outputs=[("fasta_subsequence", FeatureData[SamtoolsIndexSequencesFormat])],
    input_descriptions={
        "reference_fasta": ("Reference DNA sequence FASTA."),
        "region_file": ("File of regions.  Format is chr:from-to, one per line. Output will be a FASTA."),
        "input_fai": ("If using region_file, indexes of sequences to extract from reference FASTA."),
    },
    parameter_descriptions={
        "ignore_missing_region": (
            "Continue working if a non-existent region is requested (after trying to retrieve it)."
        ),
        "fasta_length": ("Length for output FASTA sequence line wrapping. 0 = do not line wrap."),
        "reverse_complement": (
            "Output the sequence as the reverse complement. When this option is used, “/rc” will be appended to the sequence names. "
            "To turn this off or change the string appended, use the --mark-strand option."
        ),
        "mark_strand": (
            "Add strand indicator to sequence name options: rc = /rc on negative strand (default), no = no strand indicator, "
            "sign = (+) / (-), or custom <pos>,<neg> for custom indicator."
        ),
    },
    output_descriptions={"fasta_subsequence": "Subset FASTA with formatting according to chosen parameters."},
    name="extract subsequence from FASTA using index and region files",
    description=(
        "Extract subsequence from indexed reference sequence. Subsequences will be retrieved from region_file."
        " The sequences in the reference_fasta should all have different names. If they do not, retrieval will only produce subsequences"
        " from the first sequence with the duplicated name."
    ),
)

plugin.methods.register_function(
    function=q2_samtools.index_fasta,
    inputs={
        "reference_fasta": FeatureData[Sequence]
    },
    parameters={},
    outputs=[("output_fai", FeatureData[SamtoolsIndexSequencesFormat]),
        ("dict", FeatureData[SamtoolsIndexSequencesFormat])],
    input_descriptions={
        "reference_fasta": ("Reference DNA sequence FASTA."),
    },
    parameter_descriptions={},
    output_descriptions={"output_fai": "QZA that includes both reference fasta and reference fasta index as ref.fasta.fai",
                         "dict": "The output SAM file contains a header but no SAMRecords, and the header contains only sequence records."},
    name="index a FASTA and create a dictionary",
    description=(
        "Index reference sequence in the FASTA format.fasta_index will index the file and create <ref.fasta>.fai. "
        "The sequences in the input file should all have different names. Creates a sequence dictionary for a reference sequence. This tool creates a sequence dictionary file (with .dict extension)"
        " from a reference sequence provided in FASTA format, which is required by many processing and analysis tools."
    ),
)

plugin.register_formats(SamtoolsIndexDirFormat)
plugin.register_semantic_type_to_format(FeatureData[SamtoolsIndexFormat], artifact_format=SamtoolsIndexDirFormat)
plugin.register_formats(SamtoolsRegionDirFormat)
plugin.register_semantic_type_to_format(FeatureData[SamtoolsRegionFormat], artifact_format=SamtoolsRegionDirFormat)

plugin.register_formats(SamtoolsIndexSequencesDirectoryFormat)
plugin.register_semantic_type_to_format(FeatureData[SamtoolsIndexSequencesFormat], artifact_format=SamtoolsIndexSequencesDirectoryFormat)
plugin.register_formats(DictDirFormat)
plugin.register_semantic_type_to_format(FeatureData[DictType], artifact_format=DictDirFormat)
