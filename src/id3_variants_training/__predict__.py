import argparse
import pickle
import numpy
from .ConfusionMatrix import ConfusionMatrix
from .local_API import LOCAL_API


def get_confusion_matrix(config_path, id3_tree):
    api = LOCAL_API(config_path, False)
    return ConfusionMatrix(id3_tree, api)


def predict():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', help='path to the config file that contains vcf file paths', default='config.json')
    parser.add_argument('model_file', help='path to output ID3 file', type=argparse.FileType('rb'))
    args = parser.parse_args()

    id3_model = pickle.load(args.model_file)
    conf_matrix = get_confusion_matrix(args.config_path, id3_model)
    numpy.set_printoptions(linewidth=10000)
    print(conf_matrix)
    print(conf_matrix.get_accuracy())
