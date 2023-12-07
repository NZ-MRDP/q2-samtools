import importlib
import os
import subprocess
from pathlib import Path

from q2_types.feature_data._format import DNAFASTAFormat
from qiime2.plugin import ValidationError, model


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
                                    format=DNAFASTAFormat)
    reference_fasta_index = model.File(r".+\.fasta.fai",
                                     format=SamtoolsIndexFileFormat)

    
    def _validate(self, *args):
        for fasta, fai in zip(self.fasta_file_paths, self.fai_file_paths):
            if Path(fasta).stem != Path(fai).stem:
                raise ValidationError("""Found mismatches in file names. 
                                      Bam and bai files must have matching file names before extension""")

    @reference_fasta.set_path_maker
    def fasta_path_maker(self, sample_id):
        return '%s.fasta' % sample_id
    
    @reference_fasta_index.set_path_maker
    def fai_path_maker(self, sample_id):
        return '%s.fasta.fai' % sample_id
    
    @property
    def fasta_file_paths(self):
        bound_collection = model.directory_format.BoundFileCollection(self.reference_fasta, self, path_maker=self.fasta_path_maker)
        return sorted([os.path.join(str(self.path), path) for path, _ in bound_collection.iter_views(view_type=DNAFASTAFormat)])
    
    @property
    def fai_file_paths(self):
        bound_collection = model.directory_format.BoundFileCollection(self.reference_fasta_index, self, path_maker=self.fai_path_maker)
        return sorted([os.path.join(str(self.path), path) for path, _ in bound_collection.iter_views(view_type=SamtoolsIndexFileFormat)])

