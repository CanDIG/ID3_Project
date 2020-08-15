# Case 2 - small noisy case

This test sets up a simple noisy case with three ancestries and variants
that are set up following a model.  Model code is supplied.

The files checked in were generated with

```
./noisy_test.py --ancestries 3 --samples_per_ancestry 4 --variants 4 --noise 0.2 train.vcf test.vcf ancestries.ped
```
