import argparse
import pickle
from .ConfusionMatrix import ConfusionMatrix
from .local_API import LOCAL_API

def predict():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_path', help='path to the config file that contains vcf file paths', default='config.json')
    parser.add_argument('model_file', help='path to output ID3 file', type=argparse.FileType('rb'))
    args = parser.parse_args()

    api = LOCAL_API(args.config_path, False)
    id3_tree = pickle.load(args.model_file)
    conf_matrix = ConfusionMatrix(id3_tree, api)
    print(conf_matrix)


if __name__ == '__main__':
    predict()
