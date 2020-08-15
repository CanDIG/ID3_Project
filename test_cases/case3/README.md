# Case 3 - larger noisier case

This test sets up a simple noisy case with three ancestries and variants
that are set up following a model.  Model code is supplied.

The files checked in were generated with

```
./noisy_test.py --ancestries 6 --samples_per_ancestry 15 --noise 0.33 --variants 12 ../case3/train/chr1.vcf ../case3/test/chr1.vcf ../case3/ancestries.ped
```
