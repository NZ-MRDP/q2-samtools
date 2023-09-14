import qiime2.plugin.model as model


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
