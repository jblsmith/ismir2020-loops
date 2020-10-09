# Accompanying data for music decomposition evaluation

This repository contains code and data required to recreate an evaluation discussed in [Ramires et al. 2020]((https://github.com/aframires/freesound-loop-annotator)) (in Section 6: "Music generation and decomposition").

## Purpose

Ramires et al. 2020 introduced the Freesound Loop Dataset, a set of almost 10,000 loops available [here](https://zenodo.org/record/3967852). We took random combinations of a subset of loops (constrained to have the same tempo and meter) and combined them to create short songs where the "layout" (the times of all the activated loops) was known for each.

This was ideal testing data to evaluate a loop extraction tool introduced by Smith and Goto 2018, for which there is a public implementation [here](https://github.com/jblsmith/loopextractor).

## Layout types

We took random combinations of loops and created 4 types of layout:

1. sparse: [5 drum, 5 non-drum] x 16 bars; 1 of each type always active
2. dense: [5 drum, 5 non-drum] x 16 bars; 2 of each type always active
3. factorial: [1 drum, 3 non-drum] x 30 bars; all permutations of active loops included
4. composed: [1 drum, 3 non-drum] x 32 bars; fixed design.

The first two types were invented for Ramires et al. 2020; the other two were borrowed from Smith and Goto 2018.

## Requirements

You need a copy of FSLD10K: https://zenodo.org/record/3967852

(After downloading, be sure to set the correct path for the data in `create_dataset.py`.)

You also need Python (I tested it on Python 3.7) and the packages `numpy`, `pandas` and `soundfile`.

Then just run `python create_dataset.py`.

## Citations

> Antonio Ramires, Frederic Font, Dmitry Bogdanov, Jordan B. L. Smith, Yi-Hsuan Yang, Joann Ching, Bo-Yu Chen, Yueh-Kao Wu, Hsu Wei-Han and Xavier Serra. 2020. "The Freesound Loop Dataset and Annotation Tool." Proceedings of the International Society for Music Information Retrieval (ISMIR). Montreal, QC, Canada. pp 287--294. [GitHub link](https://github.com/aframires/freesound-loop-annotator)

> Smith, Jordan B. L., and Goto, Masataka. 2018. "Nonnegative tensor factorization for source separation of loops in audio." Proceedings of the IEEE International Conference on Acoustics, Speech and Signal Processing (IEEE ICASSP). Calgary, AB, Canada. pp. 171--175. [Github link](https://github.com/jblsmith/loopextractor)