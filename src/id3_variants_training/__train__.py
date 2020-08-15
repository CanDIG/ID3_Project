from .local_API import LOCAL_API
from .ga4gh_API import GA4GH_API
from .ID3_Class import ID3
import argparse
import pickle


def train(use_local, config_path, model, diagram, verbose=True):
    if use_local:
        api = LOCAL_API(config_path, False)
    else:
        api = GA4GH_API(config_path)

    id3_tree = ID3(api, verbose)
    pickle.dump(id3_tree, model)
    if diagram:
        id3_tree.print_tree(diagram)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='path to the config file that contains variant ranges in JSON format', default='config.json')
    parser.add_argument('model_file', help='path to output ID3 file', type=argparse.FileType('wb'))
    parser.add_argument('--diagram', help='if provided, output diagram of tree to this file', type=str)
    parser.add_argument('--use-candig-apis', action='store_true', default=False,
                        help='use remote API to access variant information rather than local VCF files')

    args = parser.parse_args()
    use_local_vcf_files = not args.use_candig_apis
    config_file_path = args.config_file
    train(use_local_vcf_files, config_file_path, args.model_file, args.diagram)
