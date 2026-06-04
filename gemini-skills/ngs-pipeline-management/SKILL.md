---
name: ngs-pipeline-management
description: Next-generation sequencing pipeline management with Snakemake and Nextflow. Use for building, running, and debugging reproducible NGS workflows for RNA-seq, WGS, ChIP-seq, ATAC-seq, and amplicon sequencing. Covers pipeline design patterns, HPC/cloud execution, containerization, and workflow optimization.
allowed-tools: Read Write Edit Bash
license: MIT license
metadata:
    skill-author: Lord1Egypt
---

# NGS Pipeline Management

## Overview

NGS pipeline management involves building reproducible, scalable workflows for processing next-generation sequencing data. This skill covers Snakemake and Nextflow for workflow definition, execution on HPC clusters and cloud platforms, containerization with Docker/Singularity, and best practices for reproducible bioinformatics.

## When to Use This Skill

- Building RNA-seq, WGS, ChIP-seq, ATAC-seq, or amplicon pipelines
- Running bioinformatics workflows on SLURM/PBS/SGE clusters
- Scaling pipelines to AWS, GCP, or Azure
- Containerizing workflows with Docker or Singularity
- Debugging failed pipeline steps and log inspection
- Managing conda environments within workflows
- Parallelizing sample processing and step execution
- Generating reproducible workflow reports

## Quick Start

### Snakemake RNA-seq Pipeline

```python
# Snakefile for bulk RNA-seq analysis
SAMPLES = ["sample1", "sample2", "sample3", "sample4"]
GENOME = "GRCh38"

rule all:
    input:
        expand("results/counts/{sample}.counts.txt", sample=SAMPLES),
        "results/multiqc_report.html",

rule trim_reads:
    input:
        r1="data/raw/{sample}_R1.fastq.gz",
        r2="data/raw/{sample}_R2.fastq.gz",
    output:
        r1="data/trimmed/{sample}_R1_trimmed.fastq.gz",
        r2="data/trimmed/{sample}_R2_trimmed.fastq.gz",
        json="qc/{sample}_fastp.json",
        html="qc/{sample}_fastp.html",
    threads: 8
    shell:
        """
        fastp -i {input.r1} -I {input.r2} \
              -o {output.r1} -O {output.r2} \
              -j {output.json} -h {output.html} \
              --thread {threads} --detect_adapter_for_pe
        """

rule align_star:
    input:
        r1="data/trimmed/{sample}_R1_trimmed.fastq.gz",
        r2="data/trimmed/{sample}_R2_trimmed.fastq.gz",
        index="reference/star_index/",
    output:
        bam="results/bam/{sample}.Aligned.sortedByCoord.out.bam",
        log="results/bam/{sample}.Log.final.out",
    threads: 16
    shell:
        """
        STAR --runThreadN {threads} \
             --genomeDir {input.index} \
             --readFilesIn {input.r1} {input.r2} \
             --readFilesCommand zcat \
             --outSAMtype BAM SortedByCoordinate \
             --outSAMattributes NH HI AS NM \
             --outFileNamePrefix results/bam/{wildcards.sample}. \
             --quantMode GeneCounts
        samtools index {output.bam}
        """

rule feature_counts:
    input:
        bam="results/bam/{sample}.Aligned.sortedByCoord.out.bam",
        gtf="reference/annotation.gtf",
    output:
        counts="results/counts/{sample}.counts.txt",
    threads: 4
    shell:
        """
        featureCounts -T {threads} \
                      -a {input.gtf} \
                      -o {output.counts} \
                      -p -B -C \
                      {input.bam}
        """

rule multiqc:
    input:
        expand("qc/{sample}_fastp.json", sample=SAMPLES),
        expand("results/bam/{sample}.Log.final.out", sample=SAMPLES),
        expand("results/counts/{sample}.counts.txt", sample=SAMPLES),
    output:
        "results/multiqc_report.html",
    shell:
        "multiqc qc/ results/ -o results/ -n multiqc_report"
```

### Running Snakemake

```bash
# Dry run (check workflow without executing)
snakemake -n --snakefile Snakefile

# Local execution with 8 cores
snakemake --cores 8 --use-conda

# SLURM cluster execution
snakemake --cluster "sbatch -J {rule} -c {threads} --mem {resources.mem_mb}M -t 4:00:00" \
          --jobs 50 --use-conda --latency-wait 60

# With Singularity containers
snakemake --cores 8 --use-singularity --singularity-args "--bind /data:/data"

# Generate workflow DAG
snakemake --dag | dot -Tpdf > workflow_dag.pdf
```

### Nextflow RNA-seq Pipeline

```groovy
// main.nf — Nextflow DSL2 RNA-seq pipeline
nextflow.enable.dsl=2

params.reads = "data/raw/*_{R1,R2}.fastq.gz"
params.genome_index = "reference/star_index"
params.gtf = "reference/annotation.gtf"
params.outdir = "results"

process TRIM_READS {
    tag "$sample_id"
    publishDir "${params.outdir}/trimmed", mode: "copy"
    cpus 8

    input:
    tuple val(sample_id), path(reads)

    output:
    tuple val(sample_id), path("*_trimmed.fastq.gz"), emit: trimmed
    path "*.json", emit: json

    script:
    """
    fastp -i ${reads[0]} -I ${reads[1]} \
          -o ${sample_id}_R1_trimmed.fastq.gz \
          -O ${sample_id}_R2_trimmed.fastq.gz \
          -j ${sample_id}_fastp.json \
          --thread ${task.cpus} --detect_adapter_for_pe
    """
}

process ALIGN_STAR {
    tag "$sample_id"
    publishDir "${params.outdir}/bam", mode: "copy"
    cpus 16
    memory "48 GB"

    input:
    tuple val(sample_id), path(reads)
    path index

    output:
    tuple val(sample_id), path("*.bam"), emit: bam
    path "*.Log.final.out", emit: log

    script:
    """
    STAR --runThreadN ${task.cpus} \
         --genomeDir $index \
         --readFilesIn ${reads[0]} ${reads[1]} \
         --readFilesCommand zcat \
         --outSAMtype BAM SortedByCoordinate \
         --outFileNamePrefix ${sample_id}.
    samtools index ${sample_id}.Aligned.sortedByCoord.out.bam
    """
}

workflow {
    read_pairs = Channel.fromFilePairs(params.reads)
    genome_index = file(params.genome_index)

    trimmed = TRIM_READS(read_pairs)
    ALIGN_STAR(trimmed.trimmed, genome_index)
}
```

```bash
# Run Nextflow pipeline
nextflow run main.nf -profile docker --reads "data/raw/*_{R1,R2}.fastq.gz"

# Resume from checkpoint
nextflow run main.nf -resume

# AWS execution
nextflow run main.nf -profile awsbatch \
    --outdir s3://my-bucket/results \
    -work-dir s3://my-bucket/work
```

### Snakemake Config and Resources

```yaml
# config.yaml
samples:
  sample1:
    r1: "data/raw/sample1_R1.fastq.gz"
    r2: "data/raw/sample1_R2.fastq.gz"
  sample2:
    r1: "data/raw/sample2_R1.fastq.gz"
    r2: "data/raw/sample2_R2.fastq.gz"

genome:
  name: "GRCh38"
  star_index: "reference/star_index/"
  gtf: "reference/Homo_sapiens.GRCh38.110.gtf"
  fasta: "reference/GRCh38.fa"

params:
  fastp:
    min_length: 20
    quality: 20
  star:
    min_intron: 20
    max_intron: 1000000
```

```python
# Access config in Snakefile
configfile: "config.yaml"
SAMPLES = list(config["samples"].keys())
GTF = config["genome"]["gtf"]
STAR_INDEX = config["genome"]["star_index"]
```

### Pipeline Quality Monitoring

```python
import subprocess
import pandas as pd
import json
from pathlib import Path

def check_pipeline_status(results_dir: str) -> pd.DataFrame:
    """Check completion status of pipeline outputs."""
    results = Path(results_dir)
    status = []

    for sample_dir in sorted(results.glob("bam/*.bam")):
        sample = sample_dir.stem.split(".")[0]
        bam_size = sample_dir.stat().st_size / 1e9  # GB

        # Check STAR mapping stats
        log_file = results / f"bam/{sample}.Log.final.out"
        mapping_rate = None
        if log_file.exists():
            for line in log_file.read_text().splitlines():
                if "Uniquely mapped reads %" in line:
                    mapping_rate = float(line.split("|")[1].strip().rstrip("%"))

        status.append({
            "sample": sample,
            "bam_size_gb": round(bam_size, 2),
            "mapping_rate_%": mapping_rate,
            "status": "OK" if mapping_rate and mapping_rate > 70 else "WARN",
        })

    return pd.DataFrame(status)

status_df = check_pipeline_status("results/")
print(status_df.to_string(index=False))
print(f"\nAll passed: {(status_df['status'] == 'OK').all()}")
```

### Docker/Singularity for Reproducibility

```dockerfile
# Dockerfile for NGS pipeline tools
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    wget curl git samtools bcftools bedtools \
    && rm -rf /var/lib/apt/lists/*

# Install STAR
RUN wget https://github.com/alexdobin/STAR/releases/download/2.7.11a/STAR_2.7.11a.zip \
    && unzip STAR_2.7.11a.zip && mv STAR_2.7.11a/Linux_x86_64/STAR /usr/local/bin/

# Install conda environments
COPY envs/rnaseq.yaml .
RUN conda env create -f rnaseq.yaml

WORKDIR /data
```

```bash
# Build and use container
docker build -t ngs-pipeline:latest .
singularity pull ngs-pipeline.sif docker://ngs-pipeline:latest

# Run in Snakemake
snakemake --use-singularity \
    --singularity-args "--bind /data:/data,/reference:/reference"
```

## Pipeline Design Best Practices

| Principle | Implementation |
|-----------|---------------|
| Reproducibility | Pin tool versions in conda/Docker |
| Checkpointing | Use `-resume` (Nextflow) or `--rerun-incomplete` (Snakemake) |
| Logging | Redirect stderr to log files per rule |
| Resource management | Specify threads/memory per rule |
| Validation | `snakemake --lint` before production runs |
| Portability | Use config files, avoid hardcoded paths |

## Dependencies

```bash
# Snakemake
pip install snakemake pulp

# Nextflow
curl -s https://get.nextflow.io | bash

# Common NGS tools via conda
conda install -c bioconda star samtools featurecounts fastp multiqc
```
