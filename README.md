# ID3 Decision Tree Classifier with candig_server

[![Build Status](https://travis-ci.com/CanDIG/id3-variants-training.svg?branch=master)](https://travis-ci.com/CanDIG/id3-variants-training)

An ID3 Decision Tree Classifier that is used to interract with the candig_server (https://github.com/CanDIG/candig-server). The classifier is implemented in such a way so that it allows differential privacy to protect personal health information (PHI).

There is also a ConfusionMatrix class which is used to determine the accuracy of the decision tree.

## Quickstart

### Prerequisites

- *nix environment
- Python 3.7+

### Setup and installation

Clone the repository locally and go to the root level of the repository. Create a virtual environment and activate it:
```
python3 -m venv venv
. venv/bin/activate
```

Install the program:
```
pip install .
```

### Usage

```
usage: train-id3 [-h] [--diagram DIAGRAM] [--use-candig-apis]
                 config_file model_file

positional arguments:
  config_file        path to the config file that contains variant ranges in
                     JSON format
  model_file         path to output ID3 file

optional arguments:
  -h, --help         show this help message and exit
  --diagram DIAGRAM  if provided, output diagram of tree to this file
  --use-candig-apis  use remote API to access variant information rather than
                     local VCF files
```

```
usage: predict-id3 [-h] config_path model_file

positional arguments:
  config_path  path to the config file that contains vcf file paths
  model_file   path to output ID3 file

optional arguments:
  -h, --help   show this help message and exit
```
