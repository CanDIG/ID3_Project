#!/bin/bash
set -euo pipefail

mkdir -p train
mkdir -p trest

for infile in chr*vcf.gz
do
    base=$(basename -s .gz "${infile}")
    trainvcf="train/${base}"

    bcftools view -S samples-train.txt ${infile} > "${trainvcf}"
    bgzip "${trainvcf}"
    tabix -p vcf "${trainvcf}.gz"

    testvcf="test/${base}"

    bcftools view -S samples-test.txt ${infile} > "${testvcf}"
    bgzip "${testvcf}"
    tabix -p vcf "${testvcf}.gz"
done
