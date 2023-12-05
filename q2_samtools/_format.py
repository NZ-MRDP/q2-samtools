import qiime2.plugin.model as model
from q2_types.feature_data._format import DNAFASTAFormat


class SamtoolsIndexFileFormat(model.TextFileFormat):
    """SamtoolsIndexFileFormat."""

    # TODO: Add validation
    def _validate_(self, *args):
        pass


SamtoolsIndexDirFormat = model.SingleFileDirectoryFormat(
    "SamtoolsIndexDirFormat", "samtools_fasta_index.fai", SamtoolsIndexFileFormat
)


class SamtoolsRegionFileFormat(model.TextFileFormat):
    """SamtoolsRegionFileFormat."""

    # TODO: Add validation
    def _validate_(self, *args):
        pass


SamtoolsRegionDirFormat = model.SingleFileDirectoryFormat(
    "SamtoolsRegionDirFormat", "samtools_region_file.txt", SamtoolsRegionFileFormat
)

#TODO: add a check to make sure basename of .fasta matches basename of fasta.fai
class SamtoolsIndexSequencesDirectoryFormat(model.DirectoryFormat):
    reference_fasta = model.File(r".+\.fasta?",
                                    format=DNAFASTAFormat)
    reference_fasta_index = model.File(r".+\.fasta.fai?",
                                     format=SamtoolsIndexFileFormat)
    

