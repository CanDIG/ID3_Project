from .ConfusionMatrix import ConfusionMatrix
import argparse
from pkg_resources import resource_filename
import data


def main():
    default_file_path = resource_filename(data.__name__, 'config.json')

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', help='path to the config file that contains variant ranges in JSON format',
                        default=default_file_path)
    parser.add_argument('--use-candig-apis', action='store_true', default=False,
                        help='use remote API to access variant information rather than local VCF files')
    args = parser.parse_args()

    # Creates ConfusionMatrix object with a path to the config file and whether to use local VCF files or server VCF files
    use_local_vcf_files = not args.use_candig_apis
    conf_matrix = ConfusionMatrix(args.config_file, use_local_vcf_files)

    # prints the ConfusionMatrix
    conf_matrix.print_matrix()

    # prints the list of all the variant names
    print(conf_matrix.api.variant_name_list)

    # predicts ancestry of the person with the variant `22:50121766:50121767` and no other variant in `variant_name_list`
    conf_matrix.predict(['22:50121766:50121767'])


if __name__ == '__main__':
    main()
