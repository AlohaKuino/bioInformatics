from redun import task, File
from typing import List
import subprocess
import os

REFERENCE = "config/reference/e_coli_k12.fa"
FASTQ_DIR = "data/raw/"
OUTPUT_DIR = "data/results/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@task()
def fastqc(fastq_files: List[File]) -> None:
    cmd = f"fastqc {' '.join([f.path for f in fastq_files])} -o {OUTPUT_DIR}"
    print(f"[FastQC] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

@task()
def align_bwa(ref: File, fastq1: File, fastq2: File) -> File:
    sam_path = os.path.join(OUTPUT_DIR, "aligned.sam")
    cmd = f"bwa mem {ref.path} {fastq1.path} {fastq2.path} > {sam_path}"
    print(f"[BWA] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)
    return File(sam_path)

@task()
def convert_sam_to_bam(sam_file: File) -> File:
    bam_path = os.path.join(OUTPUT_DIR, "aligned.bam")
    cmd = f"samtools view -S -b {sam_file.path} > {bam_path}"
    print(f"[Samtools view] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)
    return File(bam_path)

@task()
def sort_bam(bam_file: File) -> File:
    sorted_bam_path = os.path.join(OUTPUT_DIR, "aligned.sorted.bam")
    cmd = f"samtools sort {bam_file.path} -o {sorted_bam_path}"
    print(f"[Samtools sort] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)
    return File(sorted_bam_path)

@task()
def flagstat(bam_file: File) -> File:
    stat_path = os.path.join(OUTPUT_DIR, "flagstat.txt")
    cmd = f"samtools flagstat {bam_file.path} > {stat_path}"
    print(f"[Samtools flagstat] Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)
    return File(stat_path)

@task()
def parse_flagstat(stat_file: File) -> float:
    result = os.popen(f"python3 scripts/parse_flagstat.py {stat_file.path}").read().strip()
    percent_mapped = float(result)
    print(f"[Parse] Percent mapped: {percent_mapped}%")
    return percent_mapped

@task()
def evaluate_mapping(percent_mapped: float) -> str:
    print(f"[PLOT] Received percent_mapped = {percent_mapped}")
    result = "OK" if percent_mapped > 90 else "not OK"
    print(f"Mapping quality: {result} ({percent_mapped:.2f}% mapped)")
    return result

@task()
def plot_mapping(percent_mapped: float) -> File:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    print(f"[Plotting] Mapping percent = {percent_mapped}")

    plt.figure(figsize=(4, 6))
    plt.bar(["Mapped", "Unmapped"], [percent_mapped, 100 - percent_mapped], color=["green", "red"])
    plt.ylabel("Percentage")
    plt.title("Read Mapping Quality")

    image_path = os.path.join(OUTPUT_DIR, "mapping_quality.png")
    plt.savefig(image_path)
    plt.close()

    return File(image_path)

@task()
def main() -> str:
    fastq1 = File(os.path.join(FASTQ_DIR, "SRR490124_1.fastq"))
    fastq2 = File(os.path.join(FASTQ_DIR, "SRR490124_2.fastq"))
    ref = File(REFERENCE)

    # Выполнение пайплайна
    fastqc([fastq1, fastq2])
    sam = align_bwa(ref, fastq1, fastq2)
    bam = convert_sam_to_bam(sam)
    sorted_bam = sort_bam(bam)
    stat_file = flagstat(sorted_bam)
    percent_mapped = parse_flagstat(stat_file)
    evaluate_mapping(percent_mapped)
    plot_file = plot_mapping(percent_mapped)
    print(f"[MAIN] Plot path: {plot_file.path}")

    return f"Pipeline completed. Plot saved to: {plot_file.path}"
