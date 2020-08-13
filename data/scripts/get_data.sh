#!/bin/bash
set -euo pipefail

tabix -h s3://1000genomes/release/20130502/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 1:101709562-101709564 1:151122488-151122490 1:159174682-159174684 > chr1.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr2.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 2:7968274-7968276 2:17362567-17362569 2:17901484-17901486 2:109513600-109513602 2:109579737-109579739 2:136707981-136707983 2:158667216-158667218 > chr2.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr3.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 3:121459588-121459590 > chr3.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr4.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 4:38815501-38815503 4:100239318-100239320 4:100244318-100244320 4:105375422-105375424 > chr4.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr5.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 5:33951692-33951694 5:170202983-170202985 > chr5.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr6.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 6:6845034-6845036 6:136482726-136482728 > chr6.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr8.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 8:28172585-28172587 8:31896591-31896593 8:110602316-110602318 8:122124301-122124303 8:145639680-145639682 > chr8.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr9.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 9:127267688-127267690 > chr9.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr10.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 10:94921064-94921066 > chr10.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr11.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 11:61597211-61597213 11:113296285-113296287 > chr11.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr12.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 12:112211832-112211834 12:112241765-112241767 > chr12.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr13.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 13:34847736-34847738 13:41715281-41715283 13:42579984-42579986 13:49070511-49070513 13:111827166-111827168 > chr13.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr14.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 14:99375320-99375322 > chr14.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr15.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 15:28197036-28197038 15:28365617-28365619 15:36220034-36220036 15:45152370-45152372 15:48426483-48426485 > chr15.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr16.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 16:89730826-89730828 > chr16.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr17.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 17:40658532-40658534 17:41056244-41056246 17:48726131-48726133 17:53568883-53568885 17:62987150-62987152 > chr17.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr18.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 18:35277621-35277623 18:40488278-40488280 18:67578930-67578932 18:67867662-67867664 > chr18.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr19.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 19:4077095-4077097 > chr19.vcf
tabix -h s3://1000genomes/release/20130502/ALL.chr20.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf.gz 20:62159503-62159505 > chr20.vcf

strip_and_compress() {
    local vcf=$1
    local chr=$( basename -s .vcf $vcf )
    out="${chr}_stripped.vcf"

    vt rminfo -t AC,AF,AN,NS,DP,EAS_AF,AMR_AF,AFR_AF,EUR_AF,SAS_AF,AA "${vcf}" | vt sort - > "${out}"
    mv "${out}" "${vcf}"
    bgzip "${vcf}"
    tabix -p vcf "${vcf}.gz"
}

for chr in  $(seq 1 22)
do
    input_vcf="chr${chr}.vcf"
    if [ -f "${input_vcf}" ]
    then
        strip_and_compress "${input_vcf}"
    fi
done
