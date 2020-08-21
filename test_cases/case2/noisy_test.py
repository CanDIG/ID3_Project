#!/usr/bin/env python3
"""
Create random data for testing classification algorithms on
"""
import argparse
import numpy
import scipy.linalg as linalg

def random_rotation_matrix(n):
    """
    Generate a random n-dimensional rotation matrix Q
    by creating a random matrix and doing a QR factorization.
    """
    rand_matrix = numpy.random.rand(n, n)
    q, _ = linalg.qr(rand_matrix)

    return q

def generate_features(patients, rotation, noise_level):
    """
    Generate random binary features, n_variants per
    patients
    """
    n_patients, n_ancestries = patients.shape
    n_variants, _ = rotation.shape

    augmented_patients = numpy.zeros((n_patients, n_variants))
    augmented_patients[:, 0:n_ancestries] = patients

    features = numpy.dot(augmented_patients, rotation)
    features += numpy.random.rand(n_patients, n_variants)*noise_level

    binarized_features = numpy.where(features < 0.5, 0, 1)
    return binarized_features


def output_vcf(outfile, features, names):
    """
    Output the features as a fake VCF
    """
    outfile.write('##fileformat=VCFv4.1\n')
    outfile.write('##FILTER=<ID=PASS,Description="All filters passed">\n')
    outfile.write('##fileDate=20200101\n')
    outfile.write('##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">\n')
    outfile.write('#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\tFORMAT\t' + '\t'.join(names) + '\n')

    chrom = 1
    rsid = '.'
    ref = 'G'
    alt = 'T'
    qual = 100
    filt = 'PASS'
    info = '.'
    fmt = 'GT'
    for rownum, row in enumerate(numpy.transpose(features)):
        pos = 100+rownum
        gts = ['1/1' if item > 0 else '0/0' for item in row]
        outfile.write(f"{chrom}\t{pos}\t{rsid}\t{ref}\t{alt}\t{qual}\t{filt}\t{info}\t{fmt}\t" + '\t'.join(gts) + '\n')


def output_ancestries(outfile, n_ancestries, samples_per):
    outfile.write("Family ID\tIndividual ID\tPaternal ID\tMaternal ID\tGender\tPhenotype\tPopulation\tRelationship\tSiblings\tSecond Order\tThird Order\tChildren\tOther Comments\n")
    noid = '.'
    gender = 1
    other = 0
    relation = 'unrel'
    for a in range(0, n_ancestries):
        ancestry = str(chr(65 + a))
        for item in range(0, 2*samples_per):
            individual_id = ancestry + str(item)
            outfile.write(f"{noid}\t{individual_id}\t{other}\t{other}\t{gender}\t{other}\t{ancestry}\t{relation}\t{other}\t{other}\t{other}\t{other}\t{other}\n")


def generate_patients(n_ancestries, samples_per, start_at=0):
    """
    Returns a matrix of patient -> ancestry assignments.
    For n_ancestries = 3, samples_per_ancestry = 2, returns

    [[1, 0, 0],
     [1, 0, 0],
     [0, 1, 0],
     [0, 1, 0],
     [0, 0, 1],
     [0, 0, 1]]
    """
    patients_mtx = numpy.zeros((n_ancestries*samples_per, n_ancestries))
    for a in range(n_ancestries):
        patients_mtx[a*samples_per:(a+1)*samples_per, a] = 1.

    names = []
    for a in range(n_ancestries):
        label = str(chr(65 + a))
        numbers = map(str, range(start_at, start_at + samples_per))
        names += [label + num for num in numbers]

    return patients_mtx, names


def main(n_ancestries, n_variants, n_samplesper, noise, trainvcf, testvcf, ancestries):
    train_patient_mtx, train_patient_labels = generate_patients(n_ancestries, n_samplesper)
    test_patient_mtx, test_patient_labels = generate_patients(n_ancestries, n_samplesper, start_at=n_samplesper)
    projection = random_rotation_matrix(n_variants)

    train_features = generate_features(train_patient_mtx, projection, noise)
    test_features = generate_features(test_patient_mtx, projection, noise)

    output_vcf(trainvcf, train_features, train_patient_labels)
    output_vcf(testvcf, test_features, test_patient_labels)
    output_ancestries(ancestries, n_ancestries, n_samplesper)



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ancestries", "-a", type=int, default=3, help="Number of ancestries")
    parser.add_argument("--samples_per_ancestry", "-s", type=int, default=10, help="Number of samples per ancestry")
    parser.add_argument("--noise", "-n", type=float, default=0.2, help="Random noise to add")
    parser.add_argument("--variants", "-v", type=int, default=4, help="Number of variants; must be larger than number of ancestries")
    parser.add_argument("train_file",  type=argparse.FileType('w'), help="File to output training data")
    parser.add_argument("test_file",  type=argparse.FileType('w'), help="File to output testing data")
    parser.add_argument("pedigree_file",  type=argparse.FileType('w'), help="File to output pedegree data")
    args = parser.parse_args()

    assert args.variants >= args.ancestries

    main(args.ancestries, args.variants, args.samples_per_ancestry, args.noise, args.train_file, args.test_file, args.pedigree_file)
