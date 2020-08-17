import argparse
import pickle
from .local_API import LOCAL_API
from .ga4gh_API import GA4GH_API
from .ID3_Class import ID3


def get_id3_tree(use_local, config_path, verbose=True):
    if use_local:
        api = LOCAL_API(config_path, False)
    else:
        api = GA4GH_API(config_path)

    return ID3(api, verbose)


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='path to the config file that contains variant ranges in JSON format', default='config.json')
    parser.add_argument('model_file', help='path to output ID3 file', type=argparse.FileType('wb'))
    parser.add_argument('--diagram', help='if provided, output diagram of tree to this file', type=str)
    parser.add_argument('--use-candig-apis', action='store_true', default=False,
                        help='use remote API to access variant information rather than local VCF files')

    args = parser.parse_args()
    use_local_vcf_files = not args.use_candig_apis
    config_file_path = args.config_file

    id3_tree = get_id3_tree(use_local_vcf_files, config_file_path)

    pickle.dump(id3_tree, args.model_file)
    if args.diagram:
        id3_tree.print_tree(args.diagram)
