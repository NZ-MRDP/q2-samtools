"""QIIME 2 plugin for running samtools."""

from setuptools import find_packages, setup

setup(
    name="q2-samtools",
    version="0.0.0",
    packages=find_packages(),
    author="Megan Chenaux, Laura Vann, Joanne Liu",
    author_email="mled@novozymes.com",
    description="QIIME2 plugin for running samtools",
    entry_points={"qiime2.plugins": ["q2-samtools=q2_samtools.plugin_setup:plugin"]},
)
