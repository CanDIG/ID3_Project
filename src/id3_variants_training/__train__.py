from .local_API import LOCAL_API
from .ga4gh_API import GA4GH_API
from .ID3_Class import ID3
import argparse
import pickle


def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', help='path to the config file that contains variant ranges in JSON format', default='config.json')
    parser.add_argument('model_file', help='path to output ID3 file', type=argparse.FileType('wb'))
    parser.add_argument('--use-candig-apis', action='store_true', default=False,
                        help='use remote API to access variant information rather than local VCF files')

    args = parser.parse_args()

    use_local_vcf_files = not args.use_candig_apis
    config_file_path = args.config_file

    if use_local_vcf_files:
        api = LOCAL_API(config_file_path, False)
    else:
        api = GA4GH_API(config_file_path)

    id3_tree = ID3(api)
    pickle.dump(id3_tree, args.model_file)


if __name__ == '__main__':
    train()
