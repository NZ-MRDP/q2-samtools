import importlib
import os
import subprocess
from pathlib import Path

from q2_types.feature_data._format import DNAFASTAFormat
from qiime2.plugin import ValidationError, model


class DictFileFormat(model.TextFileFormat):
    """DictFileFormat."""

    # TODO: Add validation
    def _validate_(self, *args):
        pass


DictDirFormat = model.SingleFileDirectoryFormat("DictDirFormat", "dna-sequences.dict", DictFileFormat)

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

class SamtoolsIndexSequencesDirectoryFormat(model.DirectoryFormat):
    reference_fasta = model.File(r".+\.fasta",
                                    format=DNAFASTAFormat),
    reference_fasta_index = model.File(r".+\.fasta.fai",
                                     format=SamtoolsIndexFileFormat),
    reference_fasta_dict = model.File(r".+\.dict", format=DictFileFormat)

    
    def _validate(self, *args):
        for fasta, fai in zip(self.reference_fasta_filepath, self.reference_fasta_index_filepath):
            if Path(fasta).stem != Path(fai).stem:
                raise ValidationError("""Found mismatches in file names. 
                                      Bam and bai files must have matching file names before extension""")

#    @reference_fasta.set_path_maker
#    def reference_fasta_path_maker(self, sample_id):
#        return '%s.fasta' % sample_id
    
#    @reference_fasta_index.set_path_maker
#    def reference_fasta_index_path_maker(self, sample_id):
#        return '%s.fasta.fai' % sample_id
    
    @property
    def reference_fasta_filepath(self):
        return [e for e in os.listdir(self.path) if e.endswith('fasta')]

    @property
    def reference_fasta_index_filepath(self):
        return [e for e in os.listdir(self.path) if e.endswith('fai')]



