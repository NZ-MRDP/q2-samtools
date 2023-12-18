from q2_types.feature_data import FeatureData
from qiime2.plugin import SemanticType

SamtoolsIndexFormat = SemanticType("SamtoolsIndexFormat", variant_of=FeatureData.field["type"])

SamtoolsRegionFormat = SemanticType("SamtoolsRegionFormat", variant_of=FeatureData.field["type"])
