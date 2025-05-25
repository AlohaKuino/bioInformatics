#!/bin/bash

REFERENCE="config/reference/e_coli_k12.fa"
FASTQ1="data/raw/SRR490124_1.fastq"
FASTQ2="data/raw/SRR490124_2.fastq"
OUTPUT_DIR="data/results"

mkdir -p $OUTPUT_DIR

# FastQC
fastqc $FASTQ1 $FASTQ2 -o $OUTPUT_DIR

# Картирование
bwa mem $REFERENCE $FASTQ1 $FASTQ2 > "$OUTPUT_DIR/aligned.sam"

# Конвертация SAM -> BAM
samtools view -S -b "$OUTPUT_DIR/aligned.sam" > "$OUTPUT_DIR/aligned.bam"

# Сортировка BAM
samtools sort "$OUTPUT_DIR/aligned.bam" -o "$OUTPUT_DIR/aligned.sorted.bam"

# Оценка качества
samtools flagstat "$OUTPUT_DIR/aligned.sorted.bam" > "$OUTPUT_DIR/flagstat.txt"

# Парсим процент маппированных ридов
PERCENT=$(grep -i "mapped.*%" "$OUTPUT_DIR/flagstat.txt" | awk '{print $4}' | tr -d '()%')
echo "Процент маппированных ридов: $PERCENT%"

# Оценка
if (( $(echo "$PERCENT > 90" | bc -l) )); then
    echo "OK"
else
    echo "not OK"
fi
