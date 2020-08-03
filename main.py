from ID3_Class import ID3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--config_file', help='Path to the config file that contains variant ranges in JSON format',
                    default='config.json')
parser.add_argument('--use_server_vcf_files', action='store_true', default=False,
                    help='Query VCF files from the server')
args = parser.parse_args()
print(not args.use_server_vcf_files)
# Creates ID3 object with a path to the config file
id3_obj = ID3(args.config_file, not args.use_server_vcf_files)

# prints the ID3 tree as `tree.png`
id3_obj.print_tree('tree')

# prints the list of all the variant names
print(id3_obj.api.variant_name_list)

# predicts ancestry of the person with the variant `22:50121766:50121767` and no other variant in `variant_name_list`
id3_obj.predict(['22:50121766:50121767'])
