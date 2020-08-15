import argparse
import pickle
import numpy
from .ConfusionMatrix import ConfusionMatrix
from .local_API import LOCAL_API

def predict(config_path, model_file):
    api = LOCAL_API(config_path, False)
    id3_tree = pickle.load(model_file)
    return ConfusionMatrix(id3_tree, api)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', help='path to the config file that contains vcf file paths', default='config.json')
    parser.add_argument('model_file', help='path to output ID3 file', type=argparse.FileType('rb'))
    args = parser.parse_args()

    conf_matrix = predict(args.config_path, args.model_file)
    numpy.set_printoptions(linewidth=10000)
    print(conf_matrix)
    print(conf_matrix.get_accuracy())