from q2_types.feature_data import FeatureData
from qiime2.plugin import SemanticType

SamtoolsIndexFormat = SemanticType("SamtoolsIndexFormat", variant_of=FeatureData.field["type"])

SamtoolsRegionFormat = SemanticType("SamtoolsRegionFormat", variant_of=FeatureData.field["type"])

SamtoolsIndexSequencesFormat = SemanticType("SamtoolsIndexSequencesFormat", variant_of=FeatureData.field["type"])

DictType = SemanticType("DictType", variant_of=FeatureData.field["type"])
