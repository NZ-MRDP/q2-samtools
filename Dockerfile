ARG Q2_TYPES_VARIANT_IMAGE=q2-types-variant:latest
FROM ${Q2_TYPES_VARIANT_IMAGE}

# Build q2-types-variant first:
# docker build ../q2-types-variant -t q2-types-variant:latest
# Then build this plugin from its own repository:
# docker build . -t q2-samtools
COPY . /plugins/q2-samtools

RUN conda install -y -c conda-forge -c bioconda gatk4 samtools && \
    conda clean -afy && \
    python -m pip install --no-cache-dir hatchling && \
    python -m pip install --no-cache-dir --no-build-isolation --no-deps /plugins/q2-samtools && \
    qiime dev refresh-cache
